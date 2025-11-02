from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.library_catalog.enums import AvailabilityEnum


class UUIDSchema(BaseModel):
    uuid: UUID


class TimestampSchema(BaseModel):
    created_at: datetime
    updated_at: datetime


class BookBase(BaseModel):
    name: str
    author: str
    year: int
    genre: str
    pages: int
    availability: AvailabilityEnum


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class Book(UUIDSchema, TimestampSchema, BookBase):
    cover_image_url: str | None
    description: str | None = None
    rating: float | None = None
