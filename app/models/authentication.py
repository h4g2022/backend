from __future__ import annotations

from app.db.base_class import Base
from app.exceptions import AppError
from sqlalchemy import Column, Index, Integer, String
from sqlalchemy import exc as SQLAlchemyExceptions
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import text


class User(Base):

    __tablename__ = "credentials"
    __table_args__ = (
        Index("username_case_sensitive_index", text("upper(username)"), unique=True),
    )

    user_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

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
    async def get_from_username(cls, session: AsyncSession, username: str):
        try:
            stmt = select(User).where(User.username.ilike(username))
            result = await session.execute(stmt)
            return result.scalars().one()

        except SQLAlchemyExceptions.NoResultFound:
            return None
