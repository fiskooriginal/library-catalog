from typing import Literal

from pydantic import BaseModel

from src.library_catalog.presentation.api.v1.schemas.base import TimestampSchema, UUIDSchema


class BookCreateRequest(BaseModel):
    name: str
    author: str
    year: int
    genre: str
    pages: int
    availability: str


class BookUpdateRequest(BaseModel):
    name: str | None = None
    author: str | None = None
    year: int | None = None
    genre: str | None = None
    pages: int | None = None
    availability: str | None = None


class BookResponse(UUIDSchema, TimestampSchema):
    name: str
    author: str
    year: int
    genre: str
    pages: int
    availability: str
    cover_image_url: str | None
    description: str | None
    rating: float | None


class PaginationQuery(BaseModel):
    offset: int = 0
    limit: int = 10


class ListBooksFilters(BaseModel):
    name: str | None = None
    author: str | None = None
    year: int | None = None
    genre: str | None = None
    pages: int | None = None
    availability: str | None = None
    year_from: int | None = None
    year_to: int | None = None
    pages_min: int | None = None
    pages_max: int | None = None
    with_metadata: bool = False
    search_mode: Literal["icontains", "exact"] = "icontains"


class ListBooksResponse(BaseModel):
    count: int
    offset: int
    limit: int
    data: list[BookResponse]
