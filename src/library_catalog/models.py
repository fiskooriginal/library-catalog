from uuid import UUID, uuid4

from sqlalchemy import DateTime, Enum, Integer, Numeric, String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column
from sqlalchemy.sql import func

from src.library_catalog.enums import AvailabilityEnum

Base = declarative_base()


class UUIDModel(Base):
    __abstract__ = True

    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)


class TimestampModel(Base):
    __abstract__ = True

    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


class Book(UUIDModel, TimestampModel):
    __tablename__ = "books"

    name: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    genre: Mapped[str] = mapped_column(String, nullable=False)
    pages: Mapped[int] = mapped_column(Integer, nullable=False)
    availability: Mapped[AvailabilityEnum] = mapped_column(
        Enum(AvailabilityEnum), default=AvailabilityEnum.IN_STOCK, nullable=False
    )
    cover_image_url: Mapped[str | None] = mapped_column(String, nullable=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    rating: Mapped[float | None] = mapped_column(Numeric(precision=3, scale=2), nullable=True)
