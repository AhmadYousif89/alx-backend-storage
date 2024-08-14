#!/usr/bin/env python3
"""Main file"""

import redis

Cache = __import__('exercise').Cache
replay_cache_hist = __import__('exercise').replay

cache = Cache()

data = b"hello"
key = cache.store(data)
print(key)

local_redis = redis.Redis()
print(local_redis.get(key))

cache.store(b"first")
print(cache.get(cache.store.__qualname__))

cache.store(b"second")
cache.store(b"third")
print(cache.get(cache.store.__qualname__))

d1 = cache.store("fourth")
print(d1)
d2 = cache.store("fifth")
print(d2)
d3 = cache.store("sixth")
print(d3)

inputs = cache._redis.lrange(f"{cache.store.__qualname__}:inputs", 0, -1)
outputs = cache._redis.lrange(f"{cache.store.__qualname__}:outputs", 0, -1)

print(f"inputs: {inputs}")
print(f"outputs: {outputs}")

TEST_CASES = {b"foo": None, 123: int, "bar": lambda d: d.decode("utf-8")}

for value, fn in TEST_CASES.items():
    key = cache.store(value)
    assert cache.get(key, fn=fn) == value

replay_cache_hist(cache.store)
