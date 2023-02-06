from datetime import datetime, timedelta
from os import environ

from app.api.deps import get_session
from app.models.authentication import User
from app.exceptions import AppError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

ACCESS_TOKEN_EXPIRE_MINUTES = 1440
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
    async def get_current_user(
        cls,
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_session),
    ):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            if username := payload.get("sub"):
                if user := await User.get_from_username(session, username):
                    return user

        except JWTError as exc:
            raise AppError.CREDENTIALS_ERROR from exc

        raise AppError.CREDENTIALS_ERROR

    @classmethod
    async def login(cls, session: AsyncSession, username: str, password: str) -> bool:
        if not (credentials := await User.get_from_username(session, username)):
            return False
        if not cls.pwd_context.verify(password, credentials.password):
            return False
        return True

    @classmethod
    async def register(
        cls, session: AsyncSession, username: str, password: str
    ) -> bool:
        account = User(
            username=username,
            password=cls.pwd_context.hash(password),
        )
        return await account.save(session)

    @classmethod
    async def verify(cls, token: str = Depends(oauth2_scheme)):
        try:
            jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            return True
        except JWTError as exc:
            raise AppError.CREDENTIALS_ERROR from exc