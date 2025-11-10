from dataclasses import dataclass
from typing import Literal

from src.library_catalog.domain.config import TEXT_MAX_LENGTH
from src.library_catalog.domain.exceptions import DomainException
from src.library_catalog.domain.vo.books import BookAvailability


@dataclass(frozen=True, slots=True, kw_only=True)
class BookFilters:
    name: str | None = None
    author: str | None = None
    year: int | None = None
    genre: str | None = None
    pages: int | None = None
    availability: BookAvailability | None = None
    year_from: int | None = None
    year_to: int | None = None
    pages_min: int | None = None
    pages_max: int | None = None
    with_metadata: bool = False
    search_mode: Literal["icontains", "exact"] = "icontains"

    def __post_init__(self) -> None:
        if self.year_from and self.year_to and self.year_from > self.year_to:
            raise DomainException("Year from must be less than year to")
        if self.pages and self.pages <= 0:
            raise DomainException("Pages must be greater than 0")
        if self.pages_min and self.pages_max and self.pages_min > self.pages_max:
            raise DomainException("Pages min must be less than pages max")
        if self.search_mode not in ["icontains", "exact"]:
            raise DomainException("Search mode must be either 'icontains' or 'exact'")
        if self.name and len(self.name) > TEXT_MAX_LENGTH:
            raise DomainException("Name must be less than 255 characters")
        if self.author and len(self.author) > TEXT_MAX_LENGTH:
            raise DomainException("Author must be less than {TEXT_MAX_LENGTH} characters")
        if self.genre and len(self.genre) > TEXT_MAX_LENGTH:
            raise DomainException("Genre must be less than {TEXT_MAX_LENGTH} characters")


@dataclass(frozen=True, slots=True, kw_only=True)
class SortSpec:
    # TODO: придумать какой-то способ один раз описать допустимые значения для сортировки
    field: Literal[
        "name",
        "author",
        "year",
        "genre",
        "pages",
        "availability",
        "created_at",
        "updated_at",
    ] = "created_at"
    direction: Literal["asc", "desc"] = "desc"

    def __post_init__(self) -> None:
        if self.field not in [
            "name",
            "author",
            "year",
            "genre",
            "pages",
            "availability",
            "created_at",
            "updated_at",
        ]:
            raise DomainException(
                "Invalid field. Allowed fields are: name, author, year, genre, pages, availability, created_at, updated_at"
            )
        if self.direction not in ["asc", "desc"]:
            raise DomainException("Invalid direction. Allowed directions are: asc, desc")
