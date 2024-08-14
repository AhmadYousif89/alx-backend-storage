#!/usr/bin/env python3
'''Writing strings to Redis.'''

from typing import Callable, Optional, Union
from functools import wraps
from uuid import uuid4
import redis


def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of calls on Cache.store"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Function to count the number of calls
        happening on the Cache.store method.

        Logic:
        - Store the count of the method in Redis using the method name.
        - Increment the count of the method by 1.
        - Call the method with the arguments passed.
        """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs for Cache.store"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Function to store the history of inputs and outputs
        happening on the Cache.store method.

        Logic:
        - Store the inputs and outputs in a list named after the method.
        - i.e, Cache.store:inputs and Cache.store:outputs
        - The inputs are stored as a string representation of the arguments
            passed to the method.
        - The outputs are stored as a string representation of the value.
        - Retrieve the inputs and outputs using the method name, "Cache.store".
        """
        self._redis.rpush(f"{method.__qualname__}:inputs", str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(f"{method.__qualname__}:outputs", output)
        return output

    return wrapper


def replay(method: Callable) -> None:
    """Display the history of calls of the Cache.store method"""

    r = redis.Redis()
    method_name = method.__qualname__
    inputs = r.lrange(f"{method_name}:inputs", 0, -1)
    outputs = r.lrange(f"{method_name}:outputs", 0, -1)
    value = r.get(method_name)
    value = value.decode("utf-8") if value else 0

    if not value:
        print(f"{method_name} was never called.")
        return

    print(f"{method_name} was called {value} times:")
    for i, (inp, outp) in enumerate(zip(inputs, outputs), 1):
        key = inp.decode('utf-8')
        value = outp.decode("utf-8")
        print(f"{method_name}(*{key}) -> {value}")


class Cache:
    """Cache class to store data in Redis"""

    def __init__(self):
        """Initialize the Redis connection"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the value in the Redis database and return the key"""
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float, None]:
        """Get the value from the Redis database"""
        value = self._redis.get(key)
        return fn(value) if fn else value

    def get_str(self, key: str) -> str:
        """Get the value from the Redis database as string"""
        value = self._redis.get(key)
        return value.decode("utf-8") if value else "(nil)"

    def get_int(self, key: str) -> int:
        """Get the value from the Redis database as integer"""
        value = self._redis.get(key)
        return int(value.decode("utf-8")) if value else 0
