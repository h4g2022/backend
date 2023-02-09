from typing import List

from fastapi import APIRouter, Depends

from app.api.deps import get_session
from app.authenticator import Authenticator
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import AppError
from app.models.talent import Talent
from app.schemas.authentication import UserType
from app.schemas.talent import TalentSchema, TalentDetailSchema, TalentBaseSchema
from app.schemas.listing import ListingSchema, ListingBaseSchema, DeletedRows
from app.models.listing import Listing
from app.models.employer import Employer

router = APIRouter()


@router.get("/all", response_model=List[ListingSchema])
async def get_all_public_listings(
    session: AsyncSession = Depends(get_session),
):
    results = await Listing.fetch_all(session)
    listings: List[ListingSchema] = []
    for row in results:
        listing = ListingSchema(**row.__dict__)
        listings.append(listing)

    return listings


@router.post("/create", response_model=ListingSchema)
async def create_listing(
    data: ListingBaseSchema,
    user: User = Depends(Authenticator.get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if user.type != UserType.employer:
        raise AppError.WRONG_USER_TYPE_ERROR
    employer = await Employer.fetch_with_uid(session, user.user_id)
    if not employer:
        raise AppError.CREDENTIALS_ERROR
    new_listing = Listing(
        employer_id=employer.employer_id,
        job_title=data.job_title,
        job_description=data.job_description,
        job_types=data.job_types,
        job_modes=data.job_modes,
        location=data.location
    )
    await new_listing.save(session)
    result = await Listing.fetch_full_with_lid(session, new_listing.listing_id)
    return ListingSchema(**result.__dict__, company=result.employer.company, email=result.employer.user.email)


@router.put("/update", response_model=ListingSchema)
async def update_listing(
    lid: int,
    data: ListingBaseSchema,
    user: User = Depends(Authenticator.get_current_user),
    session: AsyncSession = Depends(get_session)
):
    if user.type != UserType.employer:
        raise AppError.WRONG_USER_TYPE_ERROR
    employer = await Employer.fetch_with_uid(session, user.user_id)
    if not employer:
        raise AppError.CREDENTIALS_ERROR
    else:
        result = await Listing.update_with_lid(data, session, lid, user.user_id)
        return ListingSchema(**result.__dict__, company=result.employer.company, email=result.employer.user.email)


@router.delete("/delete", response_model=DeletedRows)
async def delete_listing(
    lid: int,
    user: User = Depends(Authenticator.get_current_user),
    session: AsyncSession = Depends(get_session)
):
    deleted = await Listing.delete_with_lid(session, lid, user.user_id)
    return DeletedRows(deleted_rows=deleted.rowcount)
