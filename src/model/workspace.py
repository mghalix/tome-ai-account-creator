import logging
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.model.preference import Preference
from src.model.webpage import WebPage
from src.scripts.constants import LOCATORS, URLS

logger = logging.getLogger(__name__)


class Workspace(WebPage):
    _name = __name__.split(".")[-1]
    urls: list[str] = URLS[_name]
    WORKSPACE_NAME_LOCATOR = LOCATORS[_name]["workspace_name"]
    NEXT_BUTTON_LOCATOR = LOCATORS[_name]["next_button"]

    @property
    def workspace_name(self) -> WebElement:
        try:
            return WebDriverWait(self._driver, self.WAIT_TIME).until(
                EC.presence_of_element_located(self.WORKSPACE_NAME_LOCATOR)
            )
        except TimeoutException as e:
            logger.error("Timeout while waiting for workspace name field")
            raise e

    @property
    def next(self) -> WebElement:
        try:
            return WebDriverWait(self._driver, self.WAIT_TIME).until(
                EC.presence_of_element_located(self.NEXT_BUTTON_LOCATOR)
            )
        except TimeoutException as e:
            logger.error("Timeout while waiting for next button")
            raise e

    def create_workspace(self, workspace_name: str) -> None:
        try:
            self.clearAndType(self.workspace_name, workspace_name)
            time.sleep(2)
            self.next.click()
        except Exception as e:
            logging.error(f"An error occurred while creating workspace: {e}")
            raise e

    @property
    def success(self) -> bool:
        try:
            WebDriverWait(self._driver, self.WAIT_TIME).until(
                lambda driver: any(EC.url_contains(url)(driver) for url in Preference.urls)
            )
        except:
            return False

        return True

