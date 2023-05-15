from time import sleep
import logging

from RPA.Robocorp.WorkItems import WorkItems

from scrapper import Scrapper
from data_parser import DataParser


def main():
    logger = logging.getLogger("Main Robot")
    logger.setLevel(logging.INFO)

    try:
        configuration = WorkItems().get_input_work_item().payload
        URL = configuration["url"]
        PHRASE = configuration["phrase"]
        SORT_BY = configuration["sort_by"]
        MONTHS_TO_RETRIEVE = configuration["months_to_retrieve"]
        DATE_INDEX = configuration["date_index"]
    except Exception:
        logger.exception(
            "Error getting the configuration from Robocorp Input Work Item."
        )
        return

    try:
        scrapper = Scrapper()
        scrapper.open_website(URL)
        scrapper.search_phrase(PHRASE)
        scrapper.filter_section()
        scrapper.sort_news_by(SORT_BY)
        scrapper.filter_date_range(MONTHS_TO_RETRIEVE)
        sleep(3)
        scrapper.show_more_news()
        news_webelements = scrapper.get_news_webelements()
        if not news_webelements:
            logger.info("No news found.")
            return
        image_webelements = scrapper.get_image_webelements()
    except Exception:
        logger.exception("Error scrapping the website.")
        return

    try:
        data_parser = DataParser(logger)
        news = data_parser.get_text_of_news_webelements(news_webelements)
        images_urls = data_parser.get_urls_of_image_webelements(image_webelements)
        parsed_dates = data_parser.get_parsed_dates(news, DATE_INDEX)
    except Exception:
        logger.exception("Error parsing the data.")
        return
    finally:
        scrapper.close_all_browsers()

if __name__ == "__main__":
    main()
