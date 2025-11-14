import json
from typing import Any

from src.library_catalog.infrastructure.cache.exceptions import CacheSerializationError


class CacheSerializer:
    @staticmethod
    def serialize(value: Any) -> str:
        """
        Serialize value to JSON string.

        Args:
            value: Value to serialize

        Returns:
            JSON string representation

        Raises:
            CacheSerializationError: If serialization fails
        """
        try:
            return json.dumps(value, default=str, ensure_ascii=False)
        except (TypeError, ValueError) as e:
            raise CacheSerializationError(f"Failed to serialize value: {e}") from e

    @staticmethod
    def deserialize(value: str) -> Any:
        """
        Deserialize JSON string to value.

        Args:
            value: JSON string to deserialize

        Returns:
            Deserialized value

        Raises:
            CacheSerializationError: If deserialization fails
        """
        try:
            return json.loads(value)
        except (TypeError, ValueError, json.JSONDecodeError) as e:
            raise CacheSerializationError(f"Failed to deserialize value: {e}") from e
