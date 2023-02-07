from fastapi import APIRouter, Depends
from email_validator import validate_email, EmailNotValidError

from app.api.deps import get_session
from app.authenticator import Authenticator
from app.schemas.authentication import (
    UserSchema,
    UserLoginSchema,
    UserCreateResponseSchema,
    UserLoginResponseSchema, UserRefreshSchema, UserRefreshResponseSchema,
)
from app.exceptions import AppError
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/create", response_model=UserCreateResponseSchema)
async def auth_create(data: UserSchema, session: AsyncSession = Depends(get_session)):
    await Authenticator.register(session, data.email, data.password, data.type)
    return {"email": data.email, "status": "Successfully created account."}


@router.post("/login", response_model=UserLoginResponseSchema)
async def auth_login(
    data: UserLoginSchema, session: AsyncSession = Depends(get_session)
):
    user_data = await Authenticator.login(session, data.email, data.password)
    if not user_data:
        raise AppError.WRONG_PASSWORD_ERROR

    access = Authenticator.create_access_token(data={"sub": user_data.email})
    refresh = await Authenticator.create_refresh_token(
        data={"sub": user_data.email}, session=session
    )

    return {
        "data": {"email": user_data.email, "type": user_data.type},
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=UserRefreshResponseSchema)
async def auth_refresh_token(data: UserRefreshSchema, session: AsyncSession = Depends(get_session)):
    new_access_token = await Authenticator.refresh(data.refresh_token, session)
    return {
        "access_token": new_access_token,
        "token_type": "bearer",
    }
