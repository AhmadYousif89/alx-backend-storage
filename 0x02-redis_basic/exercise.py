#!/usr/bin/env python3
"""Writing strings to Redis"""

from typing import Union
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
        key = uuid4().hex
        self._redis.set(key, data)
        return key
