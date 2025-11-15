from src.library_catalog.application.dtos.books import (
    CreateBookInput,
    ListBooksInput,
    UpdateBookInput,
)
from src.library_catalog.domain.entities.books.book import BookEntity
from src.library_catalog.domain.vo.books import BookAvailability, BookFilters, PaginationSpec, QueryResult, SortSpec
from src.library_catalog.infrastructure.utils import to_float
from src.library_catalog.presentation.api.v1.schemas.books import (
    BookCreateRequest,
    BookResponse,
    BookUpdateRequest,
    ListBooksFilters,
    ListBooksResponse,
    PaginationQuery,
)


def to_availability(value: str | None = None) -> BookAvailability | None:
    if value is None:
        return None
    try:
        return BookAvailability(value)
    except ValueError as err:
        raise ValueError(f"Invalid availability value: {value}") from err


def to_create_input(payload: BookCreateRequest) -> CreateBookInput:
    return CreateBookInput(
        name=payload.name,
        author=payload.author,
        year=payload.year,
        genre=payload.genre,
        pages=payload.pages,
        availability=to_availability(payload.availability),
    )


def to_update_input(payload: BookUpdateRequest) -> UpdateBookInput:
    return UpdateBookInput(
        name=payload.name,
        author=payload.author,
        year=payload.year,
        genre=payload.genre,
        pages=payload.pages,
        availability=to_availability(payload.availability),
    )


def to_list_input(payload: PaginationQuery, filters: ListBooksFilters) -> ListBooksInput:
    return ListBooksInput(
        filters=BookFilters(
            **filters.model_dump(exclude_none=True, exclude={"availability"}),
            availability=to_availability(filters.availability),
        ),
        page=PaginationSpec(limit=payload.limit, offset=payload.offset),
        sort=SortSpec(),
    )


def to_response(book: BookEntity) -> BookResponse:
    return BookResponse(
        uuid=book.uuid,
        created_at=book.created_at,
        updated_at=book.updated_at,
        name=book.name,
        author=book.author,
        year=book.year,
        genre=book.genre,
        pages=book.pages,
        availability=str(book.availability),
        cover_image_url=book.metadata.cover_image_url,
        description=book.metadata.description,
        rating=to_float(book.metadata.rating),
    )


def to_list_response(result: QueryResult[BookEntity]) -> ListBooksResponse:
    return ListBooksResponse(
        count=result.count,
        offset=result.offset,
        limit=result.limit,
        data=[to_response(b) for b in result.data],
    )
