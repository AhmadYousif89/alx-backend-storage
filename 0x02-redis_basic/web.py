#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import requests
import redis
import functools
from typing import Callable

# Initialize Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0)


def cache_with_expiry(expiry: int):
    """
    Wrapper function to cache the result of a function with an expiry time.
    """

    def decorator(func: Callable):
        """
        Decorator to cache the result of the function with an expiry time.
        """

        @functools.wraps(func)
        def wrapper(url: str) -> str:
            """Wrapper"""
            cache_key = f"cache:{url}"
            cached_page = redis_client.get(cache_key)
            if cached_page:
                return cached_page.decode('utf-8')
            # If not cached, fetch the page
            page_content = func(url)
            # Cache the result with expiry
            redis_client.setex(cache_key, expiry, page_content)
            return page_content

        return wrapper

    return decorator


def track_access_count(func: Callable):
    """
    Decorator to track how many times a particular URL was accessed.
    """

    @functools.wraps(func)
    def wrapper(url: str) -> str:
        count_key = f"count:{url}"
        redis_client.incr(count_key)
        return func(url)

    return wrapper


@track_access_count
@cache_with_expiry(10)
def get_page(url: str) -> str:
    """
    Fetches the HTML content of the given URL and returns it.
    """
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    return response.text


# Example usage:
if __name__ == "__main__":
    url = 'http://slowwly.robertomurray.co.uk'
    content = get_page(url)
    print(content)

    # To check how many times the URL was accessed:
    access_count = redis_client.get(f"count:{url}") or 0
    print(f"URL accessed {int(access_count)} times")
