from contextlib import suppress
from dataclasses import asdict
from uuid import UUID

from src.library_catalog.application.cache.keys.base import clean_dict, generate_hash_key
from src.library_catalog.domain.cache import CacheProtocol
from src.library_catalog.domain.cache.books import BookListCacheParams


def get_book_cache_key(uuid: UUID) -> str:
    """
    Generate cache key for a single book.

    Args:
        uuid: Book UUID

    Returns:
        Cache key in format 'book:{uuid}'
    """
    return f"book:{uuid}"


def get_books_list_cache_key(params: BookListCacheParams) -> str:
    """
    Generate cache key for books list based on filters and pagination.

    Args:
        params: BookListCacheParams with filters, pagination, and sort

    Returns:
        Cache key in format 'books:list:{hash}'
    """
    filters_dict = None
    if params.filters:
        filters_dict = clean_dict(asdict(params.filters))

    sort_dict = None
    if params.sort:
        sort_dict = asdict(params.sort)

    cache_data = {
        "filters": filters_dict,
        "page": {
            "offset": params.page.offset if params.page else 0,
            "limit": params.page.limit if params.page else 0,
        },
        "sort": sort_dict,
    }

    return generate_hash_key("books:list", cache_data)


async def invalidate_book_cache(cache: CacheProtocol, uuid: UUID) -> None:
    """
    Invalidate cache for a specific book.

    Args:
        cache: Cache instance
        uuid: Book UUID
    """
    with suppress(Exception):
        await cache.delete(get_book_cache_key(uuid))


async def invalidate_books_list_cache(cache: CacheProtocol) -> None:
    """
    Invalidate all books list cache entries.

    Args:
        cache: Cache instance
    """
    with suppress(Exception):
        await cache.delete_pattern("books:list:*")
