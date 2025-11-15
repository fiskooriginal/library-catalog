import logging
from uuid import UUID

from src.library_catalog.application.dtos.books import CreateBookInput, ListBooksInput, UpdateBookInput
from src.library_catalog.application.mappers.books import (
    create_domain_book,
    get_updated_domain_book,
    to_domain_book_list_cache_params,
)
from src.library_catalog.application.uow.books import BooksUOW
from src.library_catalog.domain.cache import BookCacheServiceProtocol
from src.library_catalog.domain.entities.books import BookEntity
from src.library_catalog.domain.exceptions.books import BookAlreadyExistsException, BookNotFoundException
from src.library_catalog.domain.gateways.books import BookMetadataGatewayProtocol
from src.library_catalog.domain.vo.books import BookMetadata, QueryResult

logger = logging.getLogger(__name__)


class CreateBookUseCase:
    def __init__(
        self, metadata_gateway: BookMetadataGatewayProtocol, uow: BooksUOW, cache: BookCacheServiceProtocol
    ) -> None:
        self._metadata_gateway = metadata_gateway
        self._uow = uow
        self._cache = cache

    async def execute(self, input: CreateBookInput) -> BookEntity:
        logger.info("Creating book", extra={"book_author": input.author, "book_name": input.name})
        async with self._uow:
            if await self._uow.books.exists(input.author, input.name):
                logger.warning(
                    "Book already exists",
                    extra={"book_author": input.author, "book_name": input.name},
                )
                raise BookAlreadyExistsException(
                    f"Book with author {input.author} and name {input.name} already exists"
                )
            metadata = await self._metadata_gateway.fetch_metadata(input.name, input.author) or BookMetadata()
            book = create_domain_book(input, metadata)
            created_book = await self._uow.books.create(book)

            await self._cache.invalidate_books_list()
            await self._cache.set_book(created_book)

            logger.info(
                "Book created successfully",
                extra={
                    "book_uuid": str(created_book.uuid),
                    "book_author": created_book.author,
                    "book_name": created_book.name,
                },
            )
            return created_book


class DeleteBookUseCase:
    def __init__(self, uow: BooksUOW, cache: BookCacheServiceProtocol):
        self._uow = uow
        self._cache = cache

    async def execute(self, uuid: UUID) -> bool:
        logger.info("Deleting book", extra={"book_uuid": str(uuid)})
        async with self._uow:
            if not (await self._uow.books.get(uuid)):
                logger.warning("Book not found for deletion", extra={"book_uuid": str(uuid)})
                raise BookNotFoundException(f"Book with UUID {uuid} not found")
            result = await self._uow.books.delete(uuid)

            await self._cache.invalidate_book(uuid)
            await self._cache.invalidate_books_list()

            logger.info("Book deleted successfully", extra={"book_uuid": str(uuid)})
            return result


class GetBookUseCase:
    def __init__(self, uow: BooksUOW, cache: BookCacheServiceProtocol):
        self._uow = uow
        self._cache = cache

    async def execute(self, uuid: UUID) -> BookEntity:
        logger.debug("Getting book", extra={"book_uuid": str(uuid)})

        cached_book = await self._cache.get_book(uuid)
        if cached_book is not None:
            return cached_book

        async with self._uow:
            book = await self._uow.books.get(uuid)
            if not book:
                logger.warning("Book not found", extra={"book_uuid": str(uuid)})
                raise BookNotFoundException(f"Book with UUID {uuid} not found")

            await self._cache.set_book(book)

            return book


class GetPaginatedBookListUseCase:
    def __init__(self, uow: BooksUOW, cache: BookCacheServiceProtocol):
        self._uow = uow
        self._cache = cache

    async def execute(self, input: ListBooksInput) -> QueryResult[BookEntity]:
        logger.debug(
            "Listing books",
            extra={
                "offset": input.page.offset if input.page else 0,
                "limit": input.page.limit if input.page else 0,
                "has_filters": input.filters is not None,
            },
        )

        cache_params = to_domain_book_list_cache_params(input)
        cached_result = await self._cache.get_books_list(cache_params)
        if cached_result is not None:
            return cached_result

        async with self._uow:
            result = await self._uow.books.list(filters=input.filters, pagination=input.page, sort=input.sort)

            await self._cache.set_books_list(cache_params, result)

            logger.debug(
                "Books listed",
                extra={"count": result.count, "returned": len(result.data)},
            )
            return result


class UpdateBookUseCase:
    def __init__(
        self, metadata_gateway: BookMetadataGatewayProtocol, uow: BooksUOW, cache: BookCacheServiceProtocol
    ) -> None:
        self._metadata_gateway = metadata_gateway
        self._uow = uow
        self._cache = cache

    async def execute(self, uuid: UUID, input: UpdateBookInput) -> BookEntity:
        logger.info("Updating book", extra={"book_uuid": str(uuid)})
        async with self._uow:
            book = await self._uow.books.get(uuid)
            if not book:
                logger.warning("Book not found for update", extra={"book_uuid": str(uuid)})
                raise BookNotFoundException(f"Book with uuid={uuid} not found")

            metadata = (
                await self._metadata_gateway.fetch_metadata(input.name or book.name, input.author or book.author)
            ) or BookMetadata()

            book = get_updated_domain_book(book, metadata, input)
            result = await self._uow.books.update(uuid, book)
            if not result:
                logger.warning("Book not found after update attempt", extra={"book_uuid": str(uuid)})
                raise BookNotFoundException(f"Book with uuid={uuid} not found")

            await self._cache.invalidate_books_list()
            await self._cache.invalidate_book(uuid)
            await self._cache.set_book(result)

            logger.info(
                "Book updated successfully",
                extra={
                    "book_uuid": str(result.uuid),
                    "book_author": result.author,
                    "book_name": result.name,
                },
            )
            return result
