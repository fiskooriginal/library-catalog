from sqlalchemy import Enum, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.library_catalog.domain.vo.books.availability import BookAvailabilityEnum
from src.library_catalog.infrastructure.persistence.models.base import TimestampModel, UUIDModel


class BookModel(UUIDModel, TimestampModel):
    __tablename__ = "books"
    __table_args__ = (UniqueConstraint("author", "name", name="uq_books_author_name"),)

    name: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    genre: Mapped[str] = mapped_column(String, nullable=False)
    pages: Mapped[int] = mapped_column(Integer, nullable=False)
    availability: Mapped[BookAvailabilityEnum] = mapped_column(
        Enum(BookAvailabilityEnum), default=BookAvailabilityEnum.IN_STOCK, nullable=False
    )
    cover_image_url: Mapped[str | None] = mapped_column(String, nullable=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    rating: Mapped[Numeric | None] = mapped_column(Numeric(precision=3, scale=2), nullable=True)
