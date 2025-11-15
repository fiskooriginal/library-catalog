from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

from src.library_catalog.domain.entities.books import BookEntity
from src.library_catalog.domain.vo.books import BookFilters, PaginationSpec, QueryResult, SortSpec


@dataclass(frozen=True, slots=True, kw_only=True)
class BookListCacheParams:
    filters: BookFilters | None = None
    page: PaginationSpec | None = None
    sort: SortSpec | None = None


class BookCacheServiceProtocol(Protocol):
    @abstractmethod
    async def get_book(self, uuid: UUID) -> BookEntity | None:
        """
        Get book from cache by UUID.

        Args:
            uuid: Book UUID

        Returns:
            BookEntity if found in cache, None otherwise (including on errors)
        """
        ...

    @abstractmethod
    async def set_book(self, book: BookEntity) -> None:
        """
        Store book in cache.

        Args:
            book: BookEntity to cache

        Note:
            Does not raise exceptions on cache write errors (graceful degradation)
        """
        ...

    @abstractmethod
    async def get_books_list(self, params: BookListCacheParams) -> QueryResult[BookEntity] | None:
        """
        Get books list from cache based on filters and pagination.

        Args:
            params: BookListCacheParams with filters, pagination, and sort

        Returns:
            QueryResult[BookEntity] if found in cache, None otherwise (including on errors)
        """
        ...

    @abstractmethod
    async def set_books_list(self, params: BookListCacheParams, result: QueryResult[BookEntity]) -> None:
        """
        Store books list in cache.

        Args:
            params: BookListCacheParams used to generate cache key
            result: QueryResult[BookEntity] to cache

        Note:
            Does not raise exceptions on cache write errors (graceful degradation)
        """
        ...

    @abstractmethod
    async def invalidate_book(self, uuid: UUID) -> None:
        """
        Invalidate cache for a specific book.

        Args:
            uuid: Book UUID

        Note:
            Does not raise exceptions on cache errors (graceful degradation)
        """
        ...

    @abstractmethod
    async def invalidate_books_list(self) -> None:
        """
        Invalidate all books list cache entries.

        Note:
            Does not raise exceptions on cache errors (graceful degradation)
        """
        ...
