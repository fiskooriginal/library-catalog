from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.library_catalog.presentation.api.v1.di.books import (
    CreateBookDep,
    DeleteBookDep,
    GetBookDep,
    ListBooksDep,
    UpdateBookDep,
)
from src.library_catalog.presentation.api.v1.mappers.books import (
    to_create_input,
    to_list_input,
    to_list_response,
    to_response,
    to_update_input,
)
from src.library_catalog.presentation.api.v1.schemas.books import (
    BookCreateRequest,
    BookResponse,
    BookUpdateRequest,
    ListBooksFilters,
    ListBooksResponse,
    PaginationQuery,
)

router = APIRouter(prefix="/books", tags=["books"])


@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(payload: BookCreateRequest, use_case: CreateBookDep):
    book = await use_case.execute(to_create_input(payload))
    return to_response(book)


@router.get("/{uuid}", response_model=BookResponse)
async def get_book(uuid: UUID, use_case: GetBookDep):
    book = await use_case.execute(uuid)
    return to_response(book)


@router.get("", response_model=ListBooksResponse)
async def list_books(
    use_case: ListBooksDep,
    p: PaginationQuery = Depends(),
    filters: ListBooksFilters = Depends(),
):
    result = await use_case.execute(to_list_input(p, filters))
    return to_list_response(result)


@router.put("/{uuid}", response_model=BookResponse)
async def update_book(uuid: UUID, payload: BookUpdateRequest, use_case: UpdateBookDep):
    book = await use_case.execute(uuid, to_update_input(payload))
    return to_response(book)


@router.delete("/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(uuid: UUID, use_case: DeleteBookDep):
    await use_case.execute(uuid)
