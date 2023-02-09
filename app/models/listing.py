from __future__ import annotations

from typing import Optional

from app.db.base_class import Base
from app.exceptions import AppError
from sqlalchemy import select, update, delete, ForeignKey, ARRAY, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload
from sqlalchemy import exc as SQLAlchemyExceptions
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.employer import Employer
from app.schemas.listing import ListingSchema, ListingBaseSchema


class Listing(Base):
    __tablename__ = "listings"

    listing_id: Mapped[int] = mapped_column(primary_key=True)
    employer_id: Mapped[int] = mapped_column(
        ForeignKey("employers.employer_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )
    job_title: Mapped[str] = mapped_column(nullable=False, server_default="")
    job_description: Mapped[str] = mapped_column(nullable=False, server_default="")
    job_types = mapped_column(ARRAY(String), nullable=False, server_default="{}")
    job_modes = mapped_column(ARRAY(String), nullable=False, server_default="{}")
    location: Mapped[str] = mapped_column(nullable=False, server_default="")
    employer: Mapped["Employer"] = relationship()

    async def save(self, session: AsyncSession):
        session.add(self)
        await session.commit()
        await session.refresh(self)
        return self

    @classmethod
    async def fetch_all(cls, session: AsyncSession):
        stmt = select(Listing)
        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def fetch_full_with_lid(
            cls, session: AsyncSession, lid: int
    ) -> Optional[ListingSchema]:
        stmt = select(Listing).where(Listing.listing_id == lid).join(Employer)
        result = await session.execute(stmt)
        return result.scalars().one()

    @classmethod
    async def update_with_lid(cls, data: ListingBaseSchema, session: AsyncSession, lid: int, uid: int):
        try:
            stmt = select(Listing).where(Listing.listing_id == lid).join(Employer).options(selectinload(Listing.employer))
            result = await session.execute(stmt)
            res = result.scalars().one()

            if res.employer.user_id != uid:
                raise AppError.NO_PERMISSION_ERROR

            stmt = (
                update(Listing)
                .returning(Listing)
                .where(Listing.listing_id == lid)
                .values(data.dict())
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalars().one()

        except SQLAlchemyExceptions.NoResultFound as exc:
            raise AppError.LISTING_NOT_EXISTS_ERROR from exc

    @classmethod
    async def delete_with_lid(cls, session: AsyncSession, lid: int, uid: int):
        try:
            stmt = select(Listing).where(Listing.listing_id == lid).join(Employer).options(selectinload(Listing.employer))
            result = await session.execute(stmt)
            res = result.scalars().one()

            if res.employer.user_id != uid:
                raise AppError.NO_PERMISSION_ERROR

            stmt = (
                delete(Listing)
                .where(Listing.listing_id == lid)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result

        except SQLAlchemyExceptions.NoResultFound as exc:
            raise AppError.LISTING_NOT_EXISTS_ERROR from exc