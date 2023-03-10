from fastapi import APIRouter, Depends

from app.api.deps import get_session
from app.authenticator import Authenticator
from app.schemas.authentication import (
    UserSchema,
    UserLoginSchema,
    UserLoginResponseSchema,
    UserRefreshSchema,
    UserRefreshResponseSchema,
    UserType, UserDataSchema, LogoutResponseSchema, StatusEnum,
)
from app.exceptions import AppError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.talent import Talent
from app.models.employer import Employer
from app.models.user import User

router = APIRouter()


@router.post("/create", response_model=UserLoginResponseSchema)
async def auth_create(data: UserSchema, session: AsyncSession = Depends(get_session)):
    res = await Authenticator.register(session, data.email, data.password, data.type)
    if res.type == UserType.talent:
        new_talent = Talent(user_id=res.user_id)
        await new_talent.save(session)
    elif res.type == UserType.employer:
        new_employer = Employer(user_id=res.user_id)
        await new_employer.save(session)

    access = Authenticator.create_access_token(data={"sub": res.email})
    refresh = await Authenticator.create_refresh_token(
        data={"sub": res.email}, session=session
    )

    return UserLoginResponseSchema(
        data=UserDataSchema(email=res.email, type=res.type),
        access_token=access,
        refresh_token=refresh,
        token_type="bearer"
    )


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
async def auth_refresh_token(
        data: UserRefreshSchema, session: AsyncSession = Depends(get_session)
):
    new_access_token, registered, user_type = await Authenticator.refresh(data.refresh_token, session)
    return UserRefreshResponseSchema(
        registered=registered,
        user_type=user_type,
        access_token=new_access_token,
        token_type="bearer"
    )


@router.post("/logout", response_model=LogoutResponseSchema)
async def log_out(
        user: User = Depends(Authenticator.get_current_user),
        session: AsyncSession = Depends(get_session)
):
    await Authenticator.logout(session, user.email)
    return LogoutResponseSchema(status=StatusEnum.success)
