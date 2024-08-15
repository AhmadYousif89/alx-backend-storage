#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker using Redis."""

import redis
import requests
from typing import Callable
from functools import wraps

# Initialize Redis client
redis_client = redis.Redis()


def cache_with_expiry(expiry=10):
    """
    Wrapper function to cache the result of a function with an expiry time.

    ### Args:
        expiry (int): Time for cache_key to expire, default is 10 seconds.
    """

    def decorator(fn: Callable):
        """
        Decorator to cache the result of the function with an expiry time.
        """

        @wraps(fn)
        def wrapper(url: str) -> str:
            """Wrapper"""
            cache_key = url
            cached_page = redis_client.get(cache_key)
            if cached_page:
                return cached_page.decode('utf-8')
            # If not cached, fetch the page
            page_content = fn(url)
            # Cache the result with expiry
            redis_client.setex(cache_key, expiry, page_content)
            return page_content

        return wrapper

    return decorator


def counter(fn: Callable):
    """
    Decorator to track how many times a particular URL was accessed.
    """

    @wraps(fn)
    def wrapper(url: str) -> str:
        count_key = f"count:{url}"
        redis_client.incr(count_key)
        return fn(url)

    return wrapper


@counter
@cache_with_expiry()
def get_page(url: str) -> str:
    """
    Fetches the HTML content of the given URL and returns it.
    """
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    return response.text


# Example usage:
if __name__ == "__main__":
    # http://slowwly.robertomurray.co.uk <== Broken link
    url = 'https://github.com/AhmadYousif89'
    print(get_page(url))

    # Check how many times the URL was accessed:
    access_count = redis_client.get(f"count:{url}")
    if not access_count:
        print("URL was never accessed.")
    else:
        print(f"URL accessed {int(access_count)} times")
