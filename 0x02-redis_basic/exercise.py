#!/usr/bin/env python3
"""Writing strings to Redis"""

from typing import Callable, Union
from uuid import uuid4
import redis


class Cache:
    """Cache class to store data in Redis"""

    def __init__(self) -> None:
        """Initialize the Redis connection"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, int, bytes, float]) -> str:
        """Store the value in the Redis database and return the key"""
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable) -> Union[str, int, bytes, float]:
        """Get the value from the Redis database"""
        value: bytes | None = self._redis.get(key)
        return fn(value) if fn else value

    def get_str(self, key: str) -> str:
        """Get the value from the Redis database as string"""
        value: bytes | None = self._redis.get(key)
        return value.decode("utf-8") if value else "(nil)"

    def get_int(self, key: str) -> int:
        """Get the value from the Redis database as integer"""
        value: bytes | None = self._redis.get(key)
        return int(value.decode("utf-8")) if value else 0
