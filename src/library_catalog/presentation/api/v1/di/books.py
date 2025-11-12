from typing import Annotated

from fastapi import Depends

from src.library_catalog.application.use_cases.books import (
    CreateBookUseCase,
    DeleteBookUseCase,
    GetBookUseCase,
    GetPaginatedBookListUseCase,
    UpdateBookUseCase,
)
from src.library_catalog.infrastructure.di.providers.gateways import get_open_library_gateway
from src.library_catalog.infrastructure.di.providers.uow import get_books_uow_sqlalchemy


def get_create_book_use_case() -> CreateBookUseCase:
    return CreateBookUseCase(get_open_library_gateway(), get_books_uow_sqlalchemy())


def get_update_book_use_case() -> UpdateBookUseCase:
    return UpdateBookUseCase(get_open_library_gateway(), get_books_uow_sqlalchemy())


def get_get_book_use_case() -> GetBookUseCase:
    return GetBookUseCase(get_books_uow_sqlalchemy())


def get_list_books_use_case() -> GetPaginatedBookListUseCase:
    return GetPaginatedBookListUseCase(get_books_uow_sqlalchemy())


def get_delete_book_use_case() -> DeleteBookUseCase:
    return DeleteBookUseCase(get_books_uow_sqlalchemy())


CreateBookDep = Annotated[CreateBookUseCase, Depends(get_create_book_use_case)]
UpdateBookDep = Annotated[UpdateBookUseCase, Depends(get_update_book_use_case)]
GetBookDep = Annotated[GetBookUseCase, Depends(get_get_book_use_case)]
ListBooksDep = Annotated[GetPaginatedBookListUseCase, Depends(get_list_books_use_case)]
DeleteBookDep = Annotated[DeleteBookUseCase, Depends(get_delete_book_use_case)]
