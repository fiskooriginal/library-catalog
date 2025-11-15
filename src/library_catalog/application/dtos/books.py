from dataclasses import dataclass

from src.library_catalog.domain.vo.books import BookAvailability, BookFilters, PaginationSpec, SortSpec


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateBookInput:
    name: str
    author: str
    year: int
    genre: str
    pages: int
    availability: BookAvailability


@dataclass(frozen=True, slots=True, kw_only=True)
class ListBooksInput:
    filters: BookFilters | None = None
    page: PaginationSpec | None = None
    sort: SortSpec | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateBookInput:
    name: str | None = None
    author: str | None = None
    year: int | None = None
    genre: str | None = None
    pages: int | None = None
    availability: BookAvailability | None = None
