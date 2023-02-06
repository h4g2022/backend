from fastapi import APIRouter, Depends
from email_validator import validate_email, EmailNotValidError

from app.api.deps import get_session
from app.authenticator import Authenticator
from app.schemas.authentication import UserSchema, UserLoginSchema
from app.exceptions import AppError
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/create")
async def auth_create(data: UserSchema, session: AsyncSession = Depends(get_session)):
    try:
        validation = validate_email(data.email, check_deliverability=True)
        email = validation.email
        await Authenticator.register(session, email, data.password, data.type)
        return {"email": data.email, "status": "Successfully created account."}
    except EmailNotValidError:
        raise AppError.EMAIL_NOT_VALID_ERROR


@router.post("/login")
async def auth_login(data: UserLoginSchema, session: AsyncSession = Depends(get_session)):
    user_data = await Authenticator.login(session, data.email, data.password)
    if not user_data:
        raise AppError.WRONG_PASSWORD_ERROR

    return {
        "data": {"email": user_data.email, "type": user_data.type},
        "access_token": Authenticator.create_access_token(data={"sub": user_data.email}),
        "token_type": "bearer",
    }


@router.post("/refresh")
async def auth_refresh_token():
    return {}
