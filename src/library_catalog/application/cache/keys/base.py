import hashlib
import json
from typing import Any


def generate_hash_key(prefix: str, data: dict[str, Any]) -> str:
    """
    Generate cache key with hash from data.

    Args:
        prefix: Key prefix (e.g., 'books:list')
        data: Data to hash

    Returns:
        Cache key in format '{prefix}:{hash}'
    """
    cache_str = json.dumps(data, sort_keys=True, default=str)
    cache_hash = hashlib.md5(cache_str.encode()).hexdigest()
    return f"{prefix}:{cache_hash}"


def clean_dict(data: dict[str, Any]) -> dict[str, Any]:
    """
    Remove None values from dictionary.

    Args:
        data: Dictionary to clean

    Returns:
        Dictionary without None values
    """
    return {k: v for k, v in data.items() if v is not None}
