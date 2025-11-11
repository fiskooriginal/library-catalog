from uuid import UUID, uuid4

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class BaseModel(DeclarativeBase):
    __abstract__ = True


class UUIDModel(BaseModel):
    __abstract__ = True

    uuid: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid4)


class TimestampModel(BaseModel):
    __abstract__ = True

    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=func.now())
    updated_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True, onupdate=func.now())
