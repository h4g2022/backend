from __future__ import annotations

from typing import Optional

from app.db.base_class import Base
from sqlalchemy import ForeignKey, select
from sqlalchemy import exc as SQLAlchemyExceptions
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import BYTEA
from uuid import UUID

from app.models.user import User


class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[UUID] = mapped_column(nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.user_id), nullable=False)
    data = mapped_column(BYTEA, nullable=False)

    async def save(self, session: AsyncSession):
        session.add(self)
        await session.commit()
        await session.refresh(self)
        return self

    @classmethod
    async def fetch_with_image_id(cls, session: AsyncSession, image_id: UUID) -> Optional[Image]:
        try:
            stmt = select(Image).where(Image.uuid == image_id)
            result = await session.execute(stmt)
            return result.scalars().one()

        except SQLAlchemyExceptions.NoResultFound:
            return None

    @classmethod
    async def verify_image(cls, session: AsyncSession, image_id: UUID, user_id: int):
        image = await cls.fetch_with_image_id(session, image_id)
        if not image:
            return False
        return image.user_id == user_id
