#!/usr/bin/env python3
'''Writing strings to Redis.'''

from typing import Callable, Optional, Union
from functools import wraps
from uuid import uuid4
import redis


class Cache:
    '''Cache class.'''

    def __init__(self):
        '''Initialize the cache.'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''Store data in the cache.'''
        key = str(uuid4())
        self._redis.set(key, data)
        return key
