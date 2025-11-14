from typing import Annotated

from fastapi import Depends

from src.library_catalog.application.uow.books import BooksUOW
from src.library_catalog.application.use_cases.books import (
    CreateBookUseCase,
    DeleteBookUseCase,
    GetBookUseCase,
    GetPaginatedBookListUseCase,
    UpdateBookUseCase,
)
from src.library_catalog.domain.gateways.books import BookMetadataGatewayProtocol
from src.library_catalog.infrastructure.di.providers.gateways import get_open_library_gateway
from src.library_catalog.infrastructure.di.providers.uow import get_books_uow


def get_create_book_use_case(
    gateway: Annotated[BookMetadataGatewayProtocol, Depends(get_open_library_gateway)],
    uow: Annotated[BooksUOW, Depends(get_books_uow)],
) -> CreateBookUseCase:
    return CreateBookUseCase(gateway, uow)


def get_update_book_use_case(
    gateway: Annotated[BookMetadataGatewayProtocol, Depends(get_open_library_gateway)],
    uow: Annotated[BooksUOW, Depends(get_books_uow)],
) -> UpdateBookUseCase:
    return UpdateBookUseCase(gateway, uow)


def get_get_book_use_case(
    uow: Annotated[BooksUOW, Depends(get_books_uow)],
) -> GetBookUseCase:
    return GetBookUseCase(uow)


def get_list_books_use_case(
    uow: Annotated[BooksUOW, Depends(get_books_uow)],
) -> GetPaginatedBookListUseCase:
    return GetPaginatedBookListUseCase(uow)


def get_delete_book_use_case(uow: Annotated[BooksUOW, Depends(get_books_uow)]) -> DeleteBookUseCase:
    return DeleteBookUseCase(uow)


CreateBookDep = Annotated[CreateBookUseCase, Depends(get_create_book_use_case)]
UpdateBookDep = Annotated[UpdateBookUseCase, Depends(get_update_book_use_case)]
GetBookDep = Annotated[GetBookUseCase, Depends(get_get_book_use_case)]
ListBooksDep = Annotated[GetPaginatedBookListUseCase, Depends(get_list_books_use_case)]
DeleteBookDep = Annotated[DeleteBookUseCase, Depends(get_delete_book_use_case)]
