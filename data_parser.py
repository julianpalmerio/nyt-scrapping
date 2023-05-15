import logging
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
