from uuid import UUID

from src.library_catalog.application.dtos.books import CreateBookInput, ListBooksInput, UpdateBookInput
from src.library_catalog.application.mappers.books import create_domain_book, get_updated_domain_book
from src.library_catalog.application.uow.books import BooksUOW
from src.library_catalog.domain.entities.books import BookEntity
from src.library_catalog.domain.exceptions.books import BookAlreadyExistsException, BookNotFoundException
from src.library_catalog.domain.gateways.books import BookMetadataGatewayProtocol
from src.library_catalog.domain.vo.books import BookMetadata, QueryResult


class CreateBookUseCase:
    def __init__(self, metadata_gateway: BookMetadataGatewayProtocol, uow: BooksUOW) -> None:
        self._metadata_gateway = metadata_gateway
        self._uow = uow

    async def execute(self, input: CreateBookInput) -> BookEntity:
        async with self._uow:
            if await self._uow.books.exists(input.author, input.name):
                raise BookAlreadyExistsException(
                    f"Book with author {input.author} and name {input.name} already exists"
                )
            metadata = (await self._metadata_gateway.fetch_metadata(input.name, input.author)) or BookMetadata()
            book = create_domain_book(input, metadata)
            return await self._uow.books.create(book)


class DeleteBookUseCase:
    def __init__(self, uow: BooksUOW):
        self._uow = uow

    async def execute(self, uuid: UUID) -> bool:
        async with self._uow:
            if not (await self._uow.books.get(uuid)):
                raise BookNotFoundException(f"Book with UUID {uuid} not found")
            return await self._uow.books.delete(uuid)


class GetBookUseCase:
    def __init__(self, uow: BooksUOW):
        self._uow = uow

    async def execute(self, uuid: UUID) -> BookEntity:
        async with self._uow:
            book = await self._uow.books.get(uuid)
            if not book:
                raise BookNotFoundException(f"Book with UUID {uuid} not found")
            return book


class GetPaginatedBookListUseCase:
    def __init__(self, uow: BooksUOW):
        self._uow = uow

    async def execute(self, input: ListBooksInput) -> QueryResult[BookEntity]:
        async with self._uow:
            return await self._uow.books.list(filters=input.filters, pagination=input.page, sort=input.sort)


class UpdateBookUseCase:
    def __init__(self, metadata_gateway: BookMetadataGatewayProtocol, uow: BooksUOW) -> None:
        self._metadata_gateway = metadata_gateway
        self._uow = uow

    async def execute(self, uuid: UUID, input: UpdateBookInput) -> BookEntity:
        async with self._uow:
            book = await self._uow.books.get(uuid)
            if not book:
                raise BookNotFoundException(f"Book with uuid={uuid} not found")
            metadata = (await self._metadata_gateway.fetch_metadata(input.name, input.author)) or BookMetadata()
            book = get_updated_domain_book(book, metadata, input)
            result = await self._uow.books.update(uuid, book)
            if not result:
                raise BookNotFoundException(f"Book with uuid={uuid} not found")
            return result
