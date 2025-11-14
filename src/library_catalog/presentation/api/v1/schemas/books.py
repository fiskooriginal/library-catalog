from datetime import datetime
from typing import Literal, Self

from pydantic import BaseModel, Field, field_validator, model_validator

from src.library_catalog.domain.config import TEXT_MAX_LENGTH
from src.library_catalog.presentation.api.v1.schemas.base import TimestampSchema, UUIDSchema


class BookCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=TEXT_MAX_LENGTH, description="Book title")
    author: str = Field(..., min_length=1, max_length=TEXT_MAX_LENGTH, description="Author name")
    year: int = Field(..., gt=0, le=datetime.now().year, description="Publication year")
    genre: str = Field(..., min_length=1, max_length=TEXT_MAX_LENGTH, description="Book genre")
    pages: int = Field(..., gt=0, description="Number of pages")
    availability: Literal["in_stock", "borrowed"] = Field(..., description="Availability status")

    @field_validator("name", "author", "genre", mode="before")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip()
        return v

    @field_validator("name", "author", "genre", mode="after")
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        if not v:
            raise ValueError("Field cannot be empty after stripping whitespace")
        return v


class BookUpdateRequest(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=TEXT_MAX_LENGTH, description="Book title")
    author: str | None = Field(None, min_length=1, max_length=TEXT_MAX_LENGTH, description="Author name")
    year: int | None = Field(None, gt=0, le=datetime.now().year, description="Publication year")
    genre: str | None = Field(None, min_length=1, max_length=TEXT_MAX_LENGTH, description="Book genre")
    pages: int | None = Field(None, gt=0, description="Number of pages")
    availability: Literal["in_stock", "borrowed"] | None = Field(None, description="Availability status")

    @field_validator("name", "author", "genre", mode="before")
    @classmethod
    def strip_whitespace(cls, v: str | None) -> str | None:
        if isinstance(v, str):
            return v.strip()
        return v

    @field_validator("name", "author", "genre", mode="after")
    @classmethod
    def validate_not_empty_if_provided(cls, v: str | None) -> str | None:
        if v is not None and not v:
            raise ValueError("Field cannot be empty after stripping whitespace")
        return v


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
    offset: int = Field(0, ge=0, description="Number of records to skip")
    limit: int = Field(10, gt=0, le=1000, description="Maximum number of records to return")

    @field_validator("limit", mode="after")
    @classmethod
    def validate_limit(cls, v: int) -> int:
        if v > 1000:
            raise ValueError("Limit cannot exceed 1000")
        return v


class ListBooksFilters(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=TEXT_MAX_LENGTH, description="Filter by book name")
    author: str | None = Field(None, min_length=1, max_length=TEXT_MAX_LENGTH, description="Filter by author name")
    year: int | None = Field(None, gt=0, le=datetime.now().year, description="Filter by publication year")
    genre: str | None = Field(None, min_length=1, max_length=TEXT_MAX_LENGTH, description="Filter by genre")
    pages: int | None = Field(None, gt=0, description="Filter by exact number of pages")
    availability: Literal["in_stock", "borrowed"] | None = Field(None, description="Filter by availability status")
    year_from: int | None = Field(None, gt=0, le=datetime.now().year, description="Filter by minimum publication year")
    year_to: int | None = Field(None, gt=0, le=datetime.now().year, description="Filter by maximum publication year")
    pages_min: int | None = Field(None, gt=0, description="Filter by minimum number of pages")
    pages_max: int | None = Field(None, gt=0, description="Filter by maximum number of pages")
    with_metadata: bool = Field(False, description="Include metadata in response")
    search_mode: Literal["icontains", "exact"] = Field("icontains", description="Search mode for text fields")

    @field_validator("name", "author", "genre", mode="before")
    @classmethod
    def strip_whitespace(cls, v: str | None) -> str | None:
        if isinstance(v, str):
            return v.strip()
        return v

    @field_validator("name", "author", "genre", mode="after")
    @classmethod
    def validate_not_empty_if_provided(cls, v: str | None) -> str | None:
        if v is not None and not v:
            raise ValueError("Field cannot be empty after stripping whitespace")
        return v

    @model_validator(mode="after")
    def validate_ranges(self) -> Self:
        """Validate that range filters are logically correct."""
        if self.year_from is not None and self.year_to is not None and self.year_from > self.year_to:
            raise ValueError(f"year_from ({self.year_from}) must be less than or equal to year_to ({self.year_to})")

        if self.pages_min is not None and self.pages_max is not None and self.pages_min > self.pages_max:
            raise ValueError(f"pages_min ({self.pages_min}) must be less than or equal to pages_max ({self.pages_max})")

        return self


class ListBooksResponse(BaseModel):
    count: int
    offset: int
    limit: int
    data: list[BookResponse]
