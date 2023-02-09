from __future__ import annotations

from typing import Optional

from app.db.base_class import Base
from app.exceptions import AppError
from sqlalchemy import select, update, ForeignKey, String, Integer
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import exc as SQLAlchemyExceptions
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.talent import TalentBaseSchema


class Talent(Base):
    __tablename__ = "talents"

    talent_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("credentials.user_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        unique=True,
    )
    story: Mapped[str] = mapped_column(nullable=False, server_default="")
    job_types = mapped_column(ARRAY(String), nullable=False, server_default="{}")
    job_modes = mapped_column(ARRAY(String), nullable=False, server_default="{}")
    job_title: Mapped[str] = mapped_column(nullable=False, server_default="")
    skills = mapped_column(ARRAY(String), nullable=False, server_default="{}")
    availability = mapped_column(ARRAY(Integer), nullable=False, server_default="{}")
    center_location: Mapped[str] = mapped_column(nullable=False, server_default="")
    weekly_hours: Mapped[int] = mapped_column(nullable=False, server_default="0")
    treatment_type: Mapped[str] = mapped_column(nullable=False, server_default="")
    photo_url: Mapped[str] = mapped_column(nullable=False, server_default="")
    is_displayed: Mapped[bool] = mapped_column(nullable=False, server_default="false")
    linkedin_url: Mapped[str] = mapped_column(nullable=False, server_default="")

    async def save(self, session: AsyncSession):
        try:
            session.add(self)
            await session.commit()
            await session.refresh(self)
            return self

        except SQLAlchemyExceptions.IntegrityError as exc:
            await session.rollback()
            raise AppError.USERNAME_EXISTS_ERROR from exc

    @classmethod
    async def fetch_with_uid(cls, session: AsyncSession, uid: int) -> Optional[Talent]:
        try:
            stmt = select(Talent).where(Talent.user_id == uid)
            result = await session.execute(stmt)
            return result.scalars().one()

        except SQLAlchemyExceptions.NoResultFound:
            return None

    @classmethod
    async def update_with_uid(
        cls, data: TalentBaseSchema, session: AsyncSession, uid: int
    ) -> Optional[Talent]:
        stmt = (
            update(Talent)
            .returning(Talent)
            .where(Talent.user_id == uid)
            .values(data.dict())
        )
        result = await session.execute(stmt)
        await session.commit()
        return result.scalars().one()

    @classmethod
    async def fetch_displayed(cls, session: AsyncSession):
        stmt = select(Talent).where(Talent.is_displayed == True)
        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def fetch_with_tid(cls, session: AsyncSession, tid: int) -> Optional[Talent]:
        try:
            stmt = select(Talent).where(Talent.talent_id == tid)
            result = await session.execute(stmt)
            return result.scalars().one()

        except SQLAlchemyExceptions.NoResultFound:
            return None

    @classmethod
    async def check_talent_reg(cls, session: AsyncSession, uid: int):
        talent = await cls.fetch_with_uid(session, uid)
        if not talent:
            raise AppError.TALENT_NOT_EXISTS_ERROR
        return (
            (talent.story != "")
            and (talent.job_types != [])
            and (talent.job_modes != [])
            and (talent.job_title != "")
            and (talent.skills != [])
            and (talent.availability != [])
        )
