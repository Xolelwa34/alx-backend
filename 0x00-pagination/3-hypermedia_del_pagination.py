#!/usr/bin/env python3
"""server class"""


import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {i: row for i, row in enumerate(dataset)}
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Returns a dictionary containing hypermedia information for paginated
        resilient to deletions between requests.

        Args:
            index (int, optional): The starting index for pagination. Defaults
            page_size (int, optional): The number of items per page. Defaults.

        Raises:
            AssertionError: If index is out of range.

        Returns:
            Dict: A dictionary containing hypermedia information.
        """

        assert index is None or 0 <= index < len(
            self.indexed_dataset()
        ), "index must be within dataset range"

        indexed_dataset = self.indexed_dataset()
        total_records = len(indexed_dataset)

        if index is None:
            index = 0

        start_index = max(0, index)
        end_index = min(start_index + page_size, total_records)

        data = [indexed_dataset[i] for i in range(start_index, end_index)]
        next_index = (start_index + page_size)
        if end_index < total_records else None

        return {
            "index": start_index,
            "data": data,
            "page_size": page_size,
            "next_index": next_index,
        }


if __name__ == "__main__":
    server = Server()

    server.indexed_dataset()

    try:
        server.get_hyper_index(300000, 100)
    except AssertionError:
        print("AssertionError raised when out of range")

    index = 3
    page_size = 2

    print("Nb items: {}".format(len(server._Server__indexed_dataset)))

    # 1- request first index
    res = server.get_hyper_index(index, page_size)
    print(res)

    # 2- request next index
    print(server.get_hyper_index(res.get("next_index"), page_size))

    # 3- remove the first index
    del server._Server__indexed_dataset[res.get("index")]
    print("Nb items: {}".format(len(server._Server__indexed_dataset)))

    # 4- request again the initial index -> the first data retrieved is not
    print(server.get_hyper_index(index, page_size))

    # 5- request again initial next index -> same data page as the request 2-
    print(server.get_hyper_index(res.get("next_index"), page_size))
