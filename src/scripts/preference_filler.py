import logging
import time

from selenium.webdriver.remote.webdriver import WebDriver

from src.model.preference import Preference

logger = logging.getLogger(__name__)


def fill(driver: WebDriver, preference_data: list[str]) -> None:
    preference = Preference(driver=driver)
    if driver.current_url not in preference.urls:
        logger.debug("Not at preference page")
        return

    logger.debug(f"At preference page: {driver.current_url}")

    if preference.at_theme_page:
        theme: str = preference_data[0][0]
        logger.debug(f"Attempting to pick theme: {theme}")
        time.sleep(2)
        preference.pick_theme(theme=theme)

    if preference.at_plan_page:
        logger.debug("Attempting to pick plan...")
        preference.pick_free_plan()

    logging.info(f"Preference status: {preference.success}")
