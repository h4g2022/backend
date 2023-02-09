from fastapi import APIRouter, Depends

from app.api.deps import get_session
from app.authenticator import Authenticator
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import AppError
from app.schemas.authentication import UserType
from app.schemas.employer import EmployerSchema, EmployerBaseSchema
from app.models.employer import Employer

router = APIRouter()


@router.get("/me", response_model=EmployerSchema)
async def get_self_employer(
        user: User = Depends(Authenticator.get_current_user),
        session: AsyncSession = Depends(get_session)
):
    if user.type != UserType.employer:
        raise AppError.WRONG_USER_TYPE_ERROR
    employer = await Employer.fetch_with_uid(session, user.user_id)
    if not employer:
        raise AppError.CREDENTIALS_ERROR
    else:
        return EmployerSchema(**employer.__dict__)


@router.put("/me", response_model=EmployerSchema)
async def update_self_listing(
        data: EmployerBaseSchema,
        user: User = Depends(Authenticator.get_current_user),
        session: AsyncSession = Depends(get_session)
):
    updated = await Employer.update_with_uid(data, session, user.user_id)
    return EmployerSchema(**updated.__dict__)
