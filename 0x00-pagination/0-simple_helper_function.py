#!/usr/bin/env python3
"""
 index_range function that takes two integer arguments page and page_size
"""

from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
     Method to retreive index_range from page to page_size
"""

 start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return (start_index, end_index)

