import logging
from typing import TypeVar

import redis.asyncio as aioredis

from src.library_catalog.domain.cache import CacheProtocol
from src.library_catalog.infrastructure.cache.exceptions import CacheConnectionError, CacheSerializationError
from src.library_catalog.infrastructure.cache.serializer import CacheSerializer

logger = logging.getLogger(__name__)

T = TypeVar("T")


class RedisCache(CacheProtocol[T]):
    def __init__(self, redis_client: aioredis.Redis) -> None:
        self._client = redis_client
        self._serializer = CacheSerializer()

    async def get(self, key: str) -> T | None:
        """
        Get value from cache by key.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found

        Raises:
            CacheConnectionError: If connection to Redis fails
            CacheSerializationError: If deserialization fails
        """
        try:
            value = await self._client.get(key)
            if value is None:
                return None

            if isinstance(value, bytes):
                value = value.decode("utf-8")
            elif not isinstance(value, str):
                logger.warning(f"Unexpected value type for key {key}: {type(value)}")
                return None

            return self._serializer.deserialize(value)
        except aioredis.ConnectionError as e:
            logger.error(f"Redis connection error while getting key {key}: {e}")
            raise CacheConnectionError(f"Failed to connect to Redis: {e}") from e
        except CacheSerializationError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error while getting key {key}: {e}")
            return None

    async def set(self, key: str, value: T, ttl: int | None = None) -> None:
        """
        Set value in cache with optional TTL.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds. None means no expiration.

        Raises:
            CacheConnectionError: If connection to Redis fails
            CacheSerializationError: If serialization fails
        """
        try:
            serialized = self._serializer.serialize(value)
            if ttl is not None:
                await self._client.setex(key, ttl, serialized)
            else:
                await self._client.set(key, serialized)
        except aioredis.ConnectionError as e:
            logger.error(f"Redis connection error while setting key {key}: {e}")
            raise CacheConnectionError(f"Failed to connect to Redis: {e}") from e
        except CacheSerializationError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error while setting key {key}: {e}")
            # Don't raise - cache failures should not break the application

    async def delete(self, key: str) -> None:
        """
        Delete value from cache by key.

        Args:
            key: Cache key

        Raises:
            CacheConnectionError: If connection to Redis fails
        """
        try:
            await self._client.delete(key)
        except aioredis.ConnectionError as e:
            logger.error(f"Redis connection error while deleting key {key}: {e}")
            raise CacheConnectionError(f"Failed to connect to Redis: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error while deleting key {key}: {e}")
            # Don't raise - cache failures should not break the application

    async def exists(self, key: str) -> bool:
        """
        Check if key exists in cache.

        Args:
            key: Cache key

        Returns:
            True if key exists, False otherwise

        Raises:
            CacheConnectionError: If connection to Redis fails
        """
        try:
            result = await self._client.exists(key)
            return bool(result)
        except aioredis.ConnectionError as e:
            logger.error(f"Redis connection error while checking key {key}: {e}")
            raise CacheConnectionError(f"Failed to connect to Redis: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error while checking key {key}: {e}")
            return False

    async def delete_pattern(self, pattern: str) -> int:
        """
        Delete all keys matching pattern.

        Args:
            pattern: Pattern to match (e.g., 'books:list:*')

        Returns:
            Number of keys deleted

        Raises:
            CacheConnectionError: If connection to Redis fails
        """
        try:
            keys = []
            async for key in self._client.scan_iter(match=pattern):
                keys.append(key)

            if not keys:
                return 0

            deleted = await self._client.delete(*keys)
            return deleted
        except aioredis.ConnectionError as e:
            logger.error(f"Redis connection error while deleting pattern {pattern}: {e}")
            raise CacheConnectionError(f"Failed to connect to Redis: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error while deleting pattern {pattern}: {e}")
            return 0
