import logging

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.model.webpage import WebPage
from src.model.workspace import Workspace
from src.scripts.constants import LOCATORS, URLS

logger = logging.getLogger(__name__)


class Profile(WebPage):
    _name = __name__.split(".")[-1]
    urls: list[str] = URLS[_name]

    FIRST_NAME_LOCATOR = LOCATORS[_name]["first_name"]
    LAST_NAME_LOCATOR = LOCATORS[_name]["last_name"]
    WORK_LOCATOR = LOCATORS[_name]["work"]
    NEXT_BUTTON_LOCATOR = LOCATORS[_name]["next_button"]
    # verify mail
    DROPDOWN_LOCATOR = LOCATORS[_name]["dropdown"]
    VERIFY_BUTTON_LOCATOR = LOCATORS[_name]["verify_button"]

    @property
    def first_name(self) -> WebElement:
        try:
            return WebDriverWait(self._driver, self.WAIT_TIME).until(
                EC.presence_of_element_located(self.FIRST_NAME_LOCATOR)
            )
        except TimeoutException as e:
            logger.error("Timeout while waiting for first name field")
            raise e

    @property
    def last_name(self) -> WebElement:
        try:
            return WebDriverWait(self._driver, self.WAIT_TIME).until(
                EC.presence_of_element_located(self.LAST_NAME_LOCATOR)
            )
        except TimeoutException as e:
            logger.error("Timeout while waiting for last name field")
            raise e

    @property
    def work(self) -> WebElement:
        try:
            return WebDriverWait(self._driver, self.WAIT_TIME).until(
                EC.presence_of_element_located(self.WORK_LOCATOR)
            )
        except TimeoutException as e:
            logger.error("Timeout while waiting for work field")
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

    @property
    def dropdown(self) -> WebElement:
        try:
            return WebDriverWait(self._driver, self.WAIT_TIME).until(
                EC.presence_of_element_located(self.DROPDOWN_LOCATOR)
            )
        except TimeoutException as e:
            logger.error("Timeout while waiting for dropdown button")
            raise e

    def create_profile(self, first_name: str, last_name: str) -> None:
        try:
            self.clearAndType(self.first_name, first_name)
            self.clearAndType(self.last_name, last_name)
            self.dropdown.click()
            self.work.click()
            self.next.click()
        except Exception as e:
            logger.error(f"An error occurred while creating profile page: {e}")
            raise e

    @property
    def verify_button(self) -> WebElement:
        try:
            return WebDriverWait(self._driver, self.WAIT_TIME).until(
                EC.presence_of_element_located(self.VERIFY_BUTTON_LOCATOR)
            )
        except TimeoutException as e:
            logger.error("Timeout while waiting for verify button")
            raise e

    def verify(self) -> None:
        try:
            self.verify_button.click()
        except Exception as e:
            logger.error(f"An error occurred while verifying email: {e}")
            raise e

    @property
    def verify_success(self) -> bool:
        try:
            WebDriverWait(self._driver, self.WAIT_TIME // 2).until(
                EC.url_changes(self.urls[1]),
            )
            return True
        except:
            return False

    @property
    def at_profile_page(self) -> bool:
        try:
            WebDriverWait(self._driver, self.WAIT_TIME).until(
                EC.url_to_be(Profile.urls[0])
            )
        except TimeoutException:
            return False

        return True

    @property
    def at_verify_page(self) -> bool:
        try:
            WebDriverWait(self._driver, self.WAIT_TIME // 2).until(
                EC.url_to_be(Profile.urls[1])
            )
        except TimeoutException:
            return False

        return True

    @property
    def success(self) -> bool:
        return self._driver.current_url in Workspace.urls
