import logging
from contextlib import suppress
from uuid import UUID

from src.library_catalog.application.cache.keys.books import (
    get_book_cache_key,
    get_books_list_cache_key,
)
from src.library_catalog.domain.cache import CacheProtocol
from src.library_catalog.domain.cache.books import BookListCacheParams
from src.library_catalog.domain.config import BOOK_CACHE_TTL, BOOKS_LIST_CACHE_TTL
from src.library_catalog.domain.entities.books import BookEntity
from src.library_catalog.domain.vo.books import QueryResult
from src.library_catalog.infrastructure.persistence.mappers.books import dict_to_domain, domain_to_json_dict

logger = logging.getLogger(__name__)


class BookCacheService:
    def __init__(self, cache: CacheProtocol) -> None:
        """
        Initialize BookCacheService.

        Args:
            cache: Cache protocol implementation
        """
        self._cache = cache

    async def get_book(self, uuid: UUID) -> BookEntity | None:
        """
        Get book from cache by UUID.

        Args:
            uuid: Book UUID

        Returns:
            BookEntity if found in cache, None otherwise (including on errors)
        """
        cache_key = get_book_cache_key(uuid)
        with suppress(Exception):
            cached_data = await self._cache.get(cache_key)
            if cached_data is not None:
                logger.debug("Book retrieved from cache", extra={"book_uuid": str(uuid)})
                return dict_to_domain(cached_data)
        return None

    async def set_book(self, book: BookEntity) -> None:
        """
        Store book in cache.

        Args:
            book: BookEntity to cache

        Note:
            Does not raise exceptions on cache write errors (graceful degradation)
        """
        cache_key = get_book_cache_key(book.uuid)
        with suppress(Exception):
            try:
                book_dict = domain_to_json_dict(book)
                await self._cache.set(cache_key, book_dict, ttl=BOOK_CACHE_TTL)
                logger.debug("Book stored in cache", extra={"book_uuid": str(book.uuid)})
            except Exception as e:
                logger.warning(
                    "Failed to store book in cache",
                    extra={"book_uuid": str(book.uuid), "error": str(e)},
                    exc_info=True,
                )

    async def get_books_list(self, params: BookListCacheParams) -> QueryResult[BookEntity] | None:
        """
        Get books list from cache based on filters and pagination.

        Args:
            params: BookListCacheParams with filters, pagination, and sort

        Returns:
            QueryResult[BookEntity] if found in cache, None otherwise (including on errors)
        """
        cache_key = get_books_list_cache_key(params)
        with suppress(Exception):
            cached_data = await self._cache.get(cache_key)
            if cached_data is not None:
                logger.debug("Books list retrieved from cache", extra={"cache_key": cache_key})
                return QueryResult[BookEntity](
                    count=cached_data["count"],
                    offset=cached_data["offset"],
                    limit=cached_data["limit"],
                    data=[dict_to_domain(book_dict) for book_dict in cached_data["data"]],
                )
        return None

    async def set_books_list(self, params: BookListCacheParams, result: QueryResult[BookEntity]) -> None:
        """
        Store books list in cache.

        Args:
            params: BookListCacheParams used to generate cache key
            result: QueryResult[BookEntity] to cache

        Note:
            Does not raise exceptions on cache write errors (graceful degradation)
        """
        cache_key = get_books_list_cache_key(params)
        with suppress(Exception):
            try:
                result_dict = {
                    "count": result.count,
                    "offset": result.offset,
                    "limit": result.limit,
                    "data": [domain_to_json_dict(book) for book in result.data],
                }
                await self._cache.set(cache_key, result_dict, ttl=BOOKS_LIST_CACHE_TTL)
                logger.debug("Books list stored in cache", extra={"cache_key": cache_key})
            except Exception as e:
                logger.warning(
                    "Failed to store books list in cache",
                    extra={"cache_key": cache_key, "error": str(e)},
                    exc_info=True,
                )

    async def invalidate_book(self, uuid: UUID) -> None:
        """
        Invalidate cache for a specific book.

        Args:
            uuid: Book UUID

        Note:
            Does not raise exceptions on cache errors (graceful degradation)
        """
        cache_key = get_book_cache_key(uuid)
        with suppress(Exception):
            try:
                await self._cache.delete(cache_key)
                logger.debug("Book cache invalidated", extra={"book_uuid": str(uuid)})
            except Exception as e:
                logger.warning(
                    "Failed to invalidate book cache",
                    extra={"book_uuid": str(uuid), "error": str(e)},
                    exc_info=True,
                )

    async def invalidate_books_list(self) -> None:
        """
        Invalidate all books list cache entries.

        Note:
            Does not raise exceptions on cache errors (graceful degradation)
        """
        with suppress(Exception):
            try:
                deleted_count = await self._cache.delete_pattern("books:list:*")
                logger.debug(
                    "Books list cache invalidated",
                    extra={"deleted_keys": deleted_count},
                )
            except Exception as e:
                logger.warning(
                    "Failed to invalidate books list cache",
                    extra={"error": str(e)},
                    exc_info=True,
                )
