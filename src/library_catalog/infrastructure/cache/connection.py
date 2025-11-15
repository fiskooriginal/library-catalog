import logging

import redis.asyncio as aioredis

from src.library_catalog.infrastructure.cache import RedisCache
from src.library_catalog.infrastructure.config import RedisSettings

logger = logging.getLogger(__name__)


def create_redis_cache(settings: RedisSettings) -> RedisCache:
    """
    Create and return Redis cache instance.

    Args:
        settings: Redis settings

    Returns:
        RedisCache instance

    Raises:
        RuntimeError: If connection to Redis fails
    """
    try:
        redis_pool = aioredis.ConnectionPool.from_url(
            settings.get_url(),
            max_connections=20,
            decode_responses=False,
        )
        redis_client = aioredis.Redis(connection_pool=redis_pool)
        return RedisCache(redis_client)
    except Exception as e:
        logger.error(f"Failed to create Redis cache: {e}")
        raise RuntimeError(f"Failed to initialize Redis cache: {e}") from e


async def close_redis_cache(cache: RedisCache) -> None:
    """
    Close Redis cache connections.

    Args:
        cache: RedisCache instance to close
    """
    try:
        redis_client = cache._client
        await redis_client.aclose()
        if hasattr(redis_client, "connection_pool") and redis_client.connection_pool:
            await redis_client.connection_pool.disconnect()
    except Exception as e:
        logger.warning(f"Error closing Redis cache: {e}")
