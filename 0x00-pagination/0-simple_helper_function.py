#!/usr/bin/env python3
"""
 index_range function that takes two integer arguments page and page_size
"""

def index_range(page, page_size):
    """
    Returns: tuple: A tuple containing the
        start index and end index for the given page.
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return start_index, end_index
