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

    def search_phrase(self, phrase: str) -> None:
        try:
            self.browser.click_element_when_visible("alias:search_button")
            self.browser.input_text_when_element_is_visible(
                "alias:search_input", phrase
            )
            self.browser.press_keys("alias:search_input", "ENTER")
        except Exception as ex:
            self.logger.error(f"Error searching the phrase {phrase}. Error: {ex}")
            raise ex

    def filter_section(self) -> None:
        # This method should be refactored to accept a list of sections
        try:
            self.browser.click_element_when_visible("alias:section_filter_button")
            self.browser.click_element_when_visible("alias:section_label_technology")
            self.browser.click_element("alias:section_filter_button")
        except AssertionError as ex:
            if "not visible after 5 seconds" in str(ex):
                self.logger.warning("The section filter is not visible.")
            else:
                self.logger.error(f"Error filtering the section. Error: {ex}")
                raise ex
        except Exception as ex:
            self.logger.error(f"Error filtering the section. Error: {ex}")
            raise ex
