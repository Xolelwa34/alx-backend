#!/usr/bin/env python3
"""Server class to paginate a database of popular baby names."""

import csv
import math
from typing import List


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Returns a page of the dataset based on page number and page size.

        Args:
            page (int, optional): The page number to retrieve. Defaults to 1.
            page_size (int, optional): The number of items per page. Defaults to 10.

        Raises:
            AssertionError: If page or page_size is not an integer greater than 0.

        Returns:
            List[List]: A list of rows representing the requested page.
        """

        assert isinstance(page, int) and page > 0, "page must be a positive integer"
        assert isinstance(page_size, int) and page_size > 0, "page_size must be a positive integer"

        dataset = self.dataset()
        total_records = len(dataset)
        total_pages = math.ceil(total_records / page_size)

        # Handle out-of-range page requests
        if page > total_pages:
            return []

        start_index, end_index = index_range(page, page_size, total_records)
        return dataset[start_index:end_index]


# Assuming index_range function is defined elsewhere (implement based on your needs)
def index_range(page: int, page_size: int, total_records: int) -> tuple:
    """
    Calculates the start and end index for pagination based on page, page_size, and total records.

    Args:
        page (int): The page number.
        page_size (int): The number of items per page.
        total_records (int): The total number of records in the dataset.

    Returns:
        tuple: A tuple containing the start and end index for the requested page.
    """
    # Implement logic to calculate start and end index based on page, page_size, and total_records
    # This function is not provided in the prompt, but you'll need to implement it based on your specific needs.
    pass


if __name__ == "__main__":
    server = Server()

    try:
        should_err = server.get_page(-10, 2)
    except AssertionError:
        print("AssertionError raised with negative values")

    try:
        should_err = server.get_page(0, 0)
    except AssertionError:
        print("AssertionError raised with 0")

    try:
        should_err = server.get_page(2, "Bob")
    except AssertionError:
        print("AssertionError raised when page and/or page_size are not ints")

    print(server.get_page(1, 3))
    print(server.get_page(3, 2))
    print(server.get_page(3000, 100))
