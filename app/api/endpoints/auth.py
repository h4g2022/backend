from fastapi import APIRouter, Depends

from app.api.deps import get_session
from app.authenticator import Authenticator
from app.schemas.authentication import (
    UserSchema,
    UserLoginSchema,
    UserCreateResponseSchema,
    UserLoginResponseSchema,
    UserRefreshSchema,
    UserRefreshResponseSchema,
    UserType,
)
from app.exceptions import AppError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.talent import Talent
from app.models.employer import Employer

router = APIRouter()


@router.post("/create", response_model=UserCreateResponseSchema)
async def auth_create(data: UserSchema, session: AsyncSession = Depends(get_session)):
    res = await Authenticator.register(session, data.email, data.password, data.type)
    if res.type == UserType.patient:
        new_talent = Talent(user_id=res.user_id)
        await new_talent.save(session)
    elif res.type == UserType.employer:
        new_employer = Employer(user_id=res.user_id)
        await new_employer.save(session)
    return {"email": res.email, "status": "Successfully created account."}


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
    new_access_token = await Authenticator.refresh(data.refresh_token, session)
    return {
        "access_token": new_access_token,
        "token_type": "bearer",
    }
