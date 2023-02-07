from __future__ import annotations

from app.db.base_class import Base
from app.exceptions import AppError
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import exc as SQLAlchemyExceptions
from sqlalchemy.ext.asyncio import AsyncSession


class User(Base):
    __tablename__ = "credentials"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)

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
    async def get_from_email(cls, session: AsyncSession, email: str):
        try:
            stmt = select(User).where(User.email.ilike(email))
            result = await session.execute(stmt)
            return result.scalars().one()

        except SQLAlchemyExceptions.NoResultFound:
            return None
