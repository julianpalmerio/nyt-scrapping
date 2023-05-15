import logging
from typing import List


class DataFormatter:
    def __init__(self, logger: logging.Logger = None) -> None:
        if logger is None:
            self.logger = logging.getLogger("DataFormatter")
        else:
            self.logger = logger

    def create_formatted_list(
        self,
        news: List[List[str]],
        parsed_dates: List[str],
        images_filenames: List[str],
        phrases_in_news: List[int],
        news_contains_money: List[bool],
        title_index: int,
        description_index: int,
        headers: List[str],
    ):
        try:
            formatted_list = [
                [
                    parsed_dates[index],
                    element[title_index],
                    element[description_index],
                    images_filenames[index],
                    phrases_in_news[index],
                    news_contains_money[index],
                ]
                for index, element in enumerate(news)
            ]
            self._insert_headers(formatted_list, headers)
            return formatted_list
        except Exception as ex:
            self.logger.exception("Error creating the formatted list.")
            raise ex

    def _insert_headers(self, data: List[List[str]], headers: List[str]):
        data.insert(0, headers)
