import logging

from RPA.Browser.Selenium import Selenium


class Scrapper:
    def __init__(self, browser: Selenium = None, logger: logging.Logger = None) -> None:
        if browser is None:
            self.browser = Selenium()
        else:
            self.browser = browser
        if logger is None:
            self.logger = logging.getLogger("Scrapper")
        else:
            self.logger = logger

    def open_website(self, url: str) -> None:
        try:
            self.browser.open_available_browser(url, headless=True)
        except Exception as ex:
            self.logger.error(f"Error opening the website {url}. Error: {ex}")
            raise ex
