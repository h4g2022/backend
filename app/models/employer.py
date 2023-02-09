from __future__ import annotations

from typing import Optional

from app.db.base_class import Base
from app.exceptions import AppError
from sqlalchemy import select, update, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import exc as SQLAlchemyExceptions
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.employer import EmployerBaseSchema


class Employer(Base):
    __tablename__ = "employers"

    employer_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("credentials.user_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        unique=True,
    )
    company: Mapped[str] = mapped_column(nullable=False, server_default="")

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
    async def fetch_with_uid(cls, session: AsyncSession, uid: int) -> Optional[Employer]:
        try:
            stmt = select(Employer).where(Employer.user_id == uid)
            result = await session.execute(stmt)
            return result.scalars().one()

        except SQLAlchemyExceptions.NoResultFound:
            return None

    @classmethod
    async def update_with_uid(
        cls, data: EmployerBaseSchema, session: AsyncSession, uid: int
    ) -> Optional[Employer]:
        stmt = (
            update(Employer)
            .returning(Employer)
            .where(Employer.user_id == uid)
            .values(data.dict())
        )
        result = await session.execute(stmt)
        await session.commit()
        return result.scalars().one()
