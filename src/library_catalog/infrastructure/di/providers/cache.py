import redis.asyncio as aioredis
from fastapi import Request

from src.library_catalog.application.cache.books import BookCacheService
from src.library_catalog.domain.cache import CacheProtocol
from src.library_catalog.domain.cache.books import BookCacheServiceProtocol


def get_redis_client(request: Request) -> aioredis.Redis:
    """
    Get Redis client from app state.

    Args:
        request: FastAPI request

    Returns:
        Redis client

    Raises:
        RuntimeError: If Redis client not initialized
    """
    if not hasattr(request.app.state, "redis_client"):
        raise RuntimeError("Redis client not initialized. Check lifespan configuration.")
    return request.app.state.redis_client


def get_cache(request: Request) -> CacheProtocol:
    """
    Get cache instance from app state.

    Args:
        request: FastAPI request

    Returns:
        Cache protocol implementation

    Raises:
        RuntimeError: If cache not initialized
    """
    if not hasattr(request.app.state, "cache"):
        raise RuntimeError("Cache not initialized. Check lifespan configuration.")
    return request.app.state.cache


def get_book_cache_service(request: Request) -> BookCacheServiceProtocol:
    """
    Get book cache service instance.

    Args:
        request: FastAPI request

    Returns:
        BookCacheServiceProtocol implementation

    Raises:
        RuntimeError: If cache not initialized
    """
    cache = get_cache(request)
    return BookCacheService(cache)
