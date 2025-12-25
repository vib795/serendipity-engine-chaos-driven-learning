"""Caching utilities."""

from functools import wraps
from typing import Callable, Any
import hashlib
import json
import pickle


def cache(ttl: int = 3600):
    """
    Simple in-memory cache decorator.
    For production, use Redis-based caching.

    Args:
        ttl: Time to live in seconds (not used in simple implementation)
    """
    _cache = {}

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            # Create cache key from function name and arguments
            key_data = {
                "func": func.__name__,
                "args": str(args),
                "kwargs": str(sorted(kwargs.items())),
            }
            cache_key = hashlib.md5(
                json.dumps(key_data, sort_keys=True).encode()
            ).hexdigest()

            # Check cache
            if cache_key in _cache:
                return _cache[cache_key]

            # Call function and cache result
            result = await func(*args, **kwargs)
            _cache[cache_key] = result

            return result

        return wrapper

    return decorator
