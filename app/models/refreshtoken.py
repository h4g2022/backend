from __future__ import annotations

from datetime import datetime

from app.db.base_class import Base
from sqlalchemy import ForeignKey, select, delete
from sqlalchemy import exc as SQLAlchemyExceptions
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(ForeignKey("credentials.email"), nullable=False)
    token: Mapped[str] = mapped_column(nullable=False, unique=True)
    expires_at: Mapped[datetime] = mapped_column(nullable=False)

    async def save(self, session: AsyncSession):
        session.add(self)
        await session.commit()
        await session.refresh(self)
        return self

    @classmethod
    async def fetch(cls, session: AsyncSession, token: str):
        try:
            stmt = select(RefreshToken).where(RefreshToken.token == token)
            result = await session.execute(stmt)
            res = result.scalars().one()

            if res.expires_at < datetime.utcnow():
                stmt = delete(RefreshToken).where(RefreshToken.token == token)
                await session.execute(stmt)
                return None

            return res

        except SQLAlchemyExceptions.NoResultFound:
            return None
