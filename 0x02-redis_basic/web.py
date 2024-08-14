#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker"""

from typing import Callable
from functools import wraps
import requests
import redis

cache = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """Decorator that increments the count for a URL"""

    @wraps(method)
    def wrapper(url):  # sourcery skip: use-named-expression
        """Wrapper for decorator"""
        cache.incr(f"count:{url}")
        cached_html = cache.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')
        html = method(url)
        cache.setex(f"cached:{url}", 10, html)
        return html

    return wrapper


@count_requests
def get_page(url: str) -> str:
    """Get the HTML content of a particular URL"""
    result = requests.get(url)
    return result.text
