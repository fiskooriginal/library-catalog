class CacheError(Exception):
    """Base exception for cache operations."""

    pass


class CacheSerializationError(CacheError):
    """Raised when serialization/deserialization fails."""

    pass


class CacheConnectionError(CacheError):
    """Raised when connection to cache fails."""

    pass
