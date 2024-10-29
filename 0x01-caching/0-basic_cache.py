#!/usr/bin/env python3
"""
Basic caching.
"""
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """
    Method that retrives and stores items from dictionary
    """
    def put(self, key, item):
        """
        Puts items in a cache
        """
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        """
        Method that uses key to retrive items
        """
        return self.cache_data.get(key, None)
