#!/usr/bin/env python3
"""Playing with Redis"""

from typing import Callable, Optional, Union
from functools import wraps
from uuid import uuid4
import redis


# def count_calls(method: Callable) -> Callable:
#     """Decorator to count the number of calls to a method"""

#     @wraps(method)
#     def wrapper(self, *args, **kwargs):
#         """Wrapper function"""
#         self._redis.incr(method.__qualname__)
#         return method(self, *args, **kwargs)

#     return wrapper


class Cache:
    """Cache class to store data in Redis"""

    def __init__(self):
        """Initialize the Redis connection"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    # @count_calls
    def store(self, data: Union[str, int, bytes, float]) -> str:
        """Store the value in the Redis database and return the key"""
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    # def get(
    #     self, key: str, fn: Optional[Callable] = None
    # ) -> Union[str, int, bytes, float, None]:
    #     """Get the value from the Redis database"""
    #     value = self._redis.get(key)
    #     return fn(value) if fn else value

    # def get_str(self, key: str) -> str:
    #     """Get the value from the Redis database as string"""
    #     value = self._redis.get(key)
    #     return value.decode("utf-8") if value else "(nil)"

    # def get_int(self, key: str) -> int:
    #     """Get the value from the Redis database as integer"""
    #     value = self._redis.get(key)
    #     return int(value.decode("utf-8")) if value else 0
