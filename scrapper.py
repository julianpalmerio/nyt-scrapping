import logging
from datetime import datetime

from dateutil.relativedelta import relativedelta
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

    def sort_news_by(self, sort_by: str) -> None:
        try:
            self.browser.select_from_list_by_value("alias:select_sort_by", sort_by)
        except Exception as ex:
            self.logger.error(f"Error sorting the news by {sort_by}. Error: {ex}")
            raise ex

    def filter_date_range(self, months_to_retrieve_option: int) -> None:
        try:
            self.browser.click_element_when_visible("alias:date_range_filter_button")
            self.browser.click_element_when_visible(
                "alias:date_range_specific_dates_button"
            )
            # There is an error in the date range filter of the web page,
            # which selects the start and end date -1 day.
            data_range = self._get_data_range(months_to_retrieve_option)
            self.browser.input_text_when_element_is_visible(
                "alias:date_range_start_date", data_range[0]
            )
            self.browser.input_text_when_element_is_visible(
                "alias:date_range_end_date", data_range[1]
            )
            self.browser.press_keys("alias:date_range_end_date", "ENTER")
        except Exception as ex:
            self.logger.error(f"Error filtering the date range. Error: {ex}")
            raise ex

    def _get_data_range(self, months_to_retrieve_option: int) -> None:
        # Get the start and end date for the date range filter
        # If the option is 1 or 0
        # then the start date is the first day of the current month
        # If the option is 2 or more
        # then the start date is the first day of the option - 1 month
        # The end date is fixed to the current date
        try:
            end_date = datetime.now().strftime("%m/%d/%Y")
            if months_to_retrieve_option <= 1:
                months = 0
            else:
                months = months_to_retrieve_option - 1
            start_date = (datetime.now() - relativedelta(months=months)).strftime(
                "%m/01/%Y"
            )
            return start_date, end_date
        except Exception as ex:
            self.logger.error(f"Error getting the date range. Error: {ex}")
            raise ex

