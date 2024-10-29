#!/usr/bin/env python3
"""
Method that operates on the principle that the first item added
 to the cache will be the first one to be removed
"""
from collections import OrderedDict

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """
     Method that retives and stores data
    """
    def __init__(self):
        """
         Initializes the cache.
        """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """
        Puts items in the cache.
        """
        if key is None or item is None:
            return
        self.cache_data[key] = item
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            first_key, _ = self.cache_data.popitem(False)
            print("DISCARD:", first_key)

    def get(self, key):
        """
         Gets an item by key.
        """
        return self.cache_data.get(key, None)
