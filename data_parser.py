import logging
from datetime import datetime
from typing import List

from selenium.webdriver.remote.webelement import WebElement


class DataParser:
    def __init__(self, logger: logging.Logger = None) -> None:
        if logger is None:
            self.logger = logging.getLogger("DataParser")
        else:
            self.logger = logger

    def get_text_of_news_webelements(
        self, news_webelements: List[WebElement]
    ) -> List[List[str]]:
        # Get the text of the news and split it into 4 columns
        # The first column is the date, the second is the section
        # The third is the title and the fourth is the description
        # The another columns are ignored
        try:
            news = [
                webelement.text.split("\n", 4)[:4] for webelement in news_webelements
            ]
            return news
        except Exception as ex:
            self.logger.error(f"Error getting the text of the news. Error: {ex}")
            raise ex

    def get_urls_of_image_webelements(
        self, image_webelements: List[WebElement]
    ) -> List[str]:
        # Get the urls of the images
        # If the image is not found, then save the url as None
        try:
            images_urls = [
                webelement.get_attribute("src") for webelement in image_webelements
            ]
            return images_urls
        except Exception as ex:
            self.logger.error(f"Error getting the image urls. Error: {ex}")
            raise ex

    def get_parsed_dates(self, news: List[List[str]], date_index: int) -> List[str]:
        try:
            dates = [new[date_index] for new in news]
            parsed_dates = [self._parse_date(date) for date in dates]
            return parsed_dates
        except Exception as ex:
            self.logger.error(f"Error parsing the dates. Error: {ex}")
            raise ex

    def _parse_date(self, date: str) -> str:
        try:
            return (
                datetime.strptime(date, "%b. %d")
                .replace(year=datetime.now().year)
                .strftime("%m/%d/%Y")
            )
        except ValueError:
            try:
                return (
                    datetime.strptime(date, "%B %d")
                    .replace(year=datetime.now().year)
                    .strftime("%m/%d/%Y")
                )
            except ValueError:
                try:
                    return datetime.strptime(date, "%b %d %Y").strftime("%m/%d/%Y")
                except ValueError:
                    self.logger.warning(
                        f"The date: '{date}' has not recognized format. "
                        "It will be saved without formatting."
                    )
                    return date

    def count_phrases_in_news(
        self, news: list, phrase: str, title_index: int, description_index: int
    ) -> List[int]:
        try:
            phrases_in_title = self._count_phrases_by_column_index(
                news, phrase, title_index
            )
            phrases_in_description = self._count_phrases_by_column_index(
                news, phrase, description_index
            )
            return [
                phrases_in_title + phrases_in_description
                for phrases_in_title, phrases_in_description in zip(
                    phrases_in_title, phrases_in_description
                )
            ]
        except Exception as ex:
            self.logger.error(f"Error counting the phrases in the news. Error: {ex}")
            raise ex

    def _count_phrases_by_column_index(
        self, news: list, phrase: str, index: int
    ) -> List[int]:
        return [self._count_phrases_in_text(element[index], phrase) for element in news]

    @staticmethod
    def _count_phrases_in_text(text: str, phrase: str) -> int:
        return text.lower().count(phrase.lower())

