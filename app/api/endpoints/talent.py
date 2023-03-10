import os
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.deps import get_session
from app.authenticator import Authenticator
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import AppError
from app.models.talent import Talent
from app.schemas.authentication import UserType
from app.schemas.talent import TalentSchema, TalentDetailSchema, TalentBaseSchema, TalentEditSchema, TalentFullSchema
from app.models.image import Image

router = APIRouter()


@router.get("/all", response_model=List[TalentSchema])
async def get_all_public_talents(
    user: User = Depends(Authenticator.get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if user.type != UserType.employer:
        raise AppError.WRONG_USER_TYPE_ERROR
    else:
        results = await Talent.fetch_displayed(session)
        listings: List[TalentSchema] = []
        for row in results:
            listing = TalentSchema(**row.__dict__)
            listings.append(listing)

    return listings


@router.get("/detail", response_model=TalentDetailSchema)
async def get_detailed_public_talent(
    tid: int,
    user: User = Depends(Authenticator.get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if user.type != UserType.employer:
        raise AppError.WRONG_USER_TYPE_ERROR
    talent = await Talent.fetch_with_tid(session, tid)
    if not talent:
        raise AppError.TALENT_NOT_EXISTS_ERROR
    else:
        return TalentDetailSchema(**talent.__dict__, email=talent.user.email)


@router.get("/me", response_model=TalentDetailSchema)
async def get_self_talent(
    user: User = Depends(Authenticator.get_current_user),
    session: AsyncSession = Depends(get_session)
):
    if user.type != UserType.talent:
        raise AppError.WRONG_USER_TYPE_ERROR
    talent = await Talent.fetch_with_uid(session, user.user_id)
    if not talent:
        raise AppError.CREDENTIALS_ERROR
    else:
        return TalentDetailSchema(**talent.__dict__)


def is_valid_uuid(value: str):
    try:
        UUID(value)
        return True
    except ValueError:
        return False

@router.put("/me", response_model=TalentSchema)
async def update_self_talent(
    data: TalentEditSchema,
    user: User = Depends(Authenticator.get_current_user),
    session: AsyncSession = Depends(get_session)
):

    if is_valid_uuid(data.photo_id):
        if not await Image.verify_image(session, data.photo_id, user.user_id):
            raise AppError.IMAGE_NOT_EXISTS_ERROR
        image_url = f"{os.environ['IMAGE_URL']}/{data.photo_id}"
        data = TalentFullSchema(**data.dict(), photo_url=image_url)
    else:
        if data.photo_id != "":
            raise AppError.IMAGE_NOT_EXISTS_ERROR
        else:
            data = TalentFullSchema(**data.dict(), photo_url="")
    updated = await Talent.update_with_uid(data, session, user.user_id)
    return TalentSchema(**updated.__dict__)
