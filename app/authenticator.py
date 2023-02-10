from datetime import datetime, timedelta
from os import environ
from typing import Optional

from app.api.deps import get_session
from app.models.user import User
from app.models.refreshtoken import RefreshToken
from app.exceptions import AppError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.authentication import UserType, UserDataSchema
from app.models.employer import Employer
from app.models.talent import Talent

ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_MINUTES = 1440
ALGORITHM = "HS256"
SECRET_KEY = environ["SECRET_KEY"]


class Authenticator:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

    @classmethod
    def create_access_token(cls, data: dict):
        expiry = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        return jwt.encode({**data, "exp": expiry}, SECRET_KEY, algorithm=ALGORITHM)

    @classmethod
    async def create_refresh_token(
        cls, data: dict, session: AsyncSession = Depends(get_session)
    ):
        expiry = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        token = jwt.encode({**data, "exp": expiry}, SECRET_KEY, algorithm=ALGORITHM)
        new_token = RefreshToken(email=data["sub"], token=token, expires_at=expiry)
        await new_token.save(session)
        return token

    @classmethod
    async def get_current_user(
        cls,
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_session),
    ):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            if email := payload.get("sub"):
                if user := await User.get_from_email(session, email):
                    return user

        except JWTError as exc:
            raise AppError.CREDENTIALS_ERROR from exc

        raise AppError.CREDENTIALS_ERROR

    @classmethod
    async def login(
        cls, session: AsyncSession, email: str, password: str
    ) -> Optional[UserDataSchema]:
        if not (credentials := await User.get_from_email(session, email)):
            return None
        if not cls.pwd_context.verify(password, credentials.password):
            return None
        return UserDataSchema(email=credentials.email, type=credentials.type)

    @classmethod
    async def register(
        cls, session: AsyncSession, email: str, password: str, type: UserType
    ) -> User:
        account = User(email=email, password=cls.pwd_context.hash(password), type=type)
        return await account.save(session)

    @classmethod
    async def verify(cls, token: str = Depends(oauth2_scheme)):
        try:
            jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            return True
        except JWTError as exc:
            raise AppError.CREDENTIALS_ERROR from exc

    @classmethod
    async def refresh(
        cls,
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_session),
    ):
        res = await RefreshToken.fetch(session, token)
        if not res:
            raise AppError.CREDENTIALS_ERROR
        else:
            user = await User.get_from_email(session, res.email)
            if not user:
                raise AppError.CREDENTIALS_ERROR
            registered = False
            if user.type == UserType.patient:
                registered = await Talent.check_talent_reg(session, user.user_id)
            elif user.type == UserType.employer:
                registered = await Employer.check_employer_reg(session, user.user_id)
            return cls.create_access_token({"sub": res.email}), registered, user.type

    @classmethod
    async def logout(cls, session: AsyncSession, email: str):
        await RefreshToken.delete_from_email(session, email)
