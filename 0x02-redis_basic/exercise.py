#!/usr/bin/env python3
'''Writing strings to Redis.'''

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
