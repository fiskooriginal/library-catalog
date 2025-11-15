from abc import abstractmethod
from typing import Protocol, TypeVar

T = TypeVar("T")


class CacheProtocol(Protocol[T]):
    @abstractmethod
    async def get(self, key: str) -> T | None:
        """
        Get value from cache by key.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found
        """
        ...

    @abstractmethod
    async def set(self, key: str, value: T, ttl: int | None = None) -> None:
        """
        Set value in cache with optional TTL.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds. None means no expiration.
        """
        ...

    @abstractmethod
    async def delete(self, key: str) -> None:
        """
        Delete value from cache by key.

        Args:
            key: Cache key
        """
        ...

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """
        Check if key exists in cache.

        Args:
            key: Cache key

        Returns:
            True if key exists, False otherwise
        """
        ...

    @abstractmethod
    async def delete_pattern(self, pattern: str) -> int:
        """
        Delete all keys matching pattern.

        Args:
            pattern: Pattern to match (e.g., 'books:list:*')

        Returns:
            Number of keys deleted
        """
        ...
