import logging

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.model.profile import Profile
from src.model.webpage import WebPage
from src.scripts.constants import LOCATORS, URLS

logger = logging.getLogger(__name__)


class Register(WebPage):
    _name = __name__.split(".")[-1]
    url: str = URLS[_name]
    EMAIL_LOCATOR = LOCATORS[_name]["email"]
    PASSWORD_LOCATOR = LOCATORS[_name]["password"]
    CONTINUE_BUTTON_LOCATOR = LOCATORS[_name]["continue_button"]

    @property
    def email(self) -> WebElement:
        try:
            return WebDriverWait(self._driver, self.WAIT_TIME).until(
                EC.presence_of_element_located(self.EMAIL_LOCATOR)
            )
        except TimeoutException as e:
            logger.error("Timeout while waiting for email field")
            raise e

    @property
    def password(self) -> WebElement:
        try:
            return WebDriverWait(self._driver, self.WAIT_TIME).until(
                EC.presence_of_element_located(self.PASSWORD_LOCATOR)
            )
        except TimeoutException as e:
            logger.error("Timeout while waiting for password field")
            raise e

    @property
    def continue_button(self) -> WebElement:
        try:
            return WebDriverWait(self._driver, self.WAIT_TIME).until(
                EC.presence_of_element_located(self.CONTINUE_BUTTON_LOCATOR)
            )
        except TimeoutException as e:
            logger.error("Timeout while waiting for continue button")
            raise e

    def register(self, email: str, password: str) -> None:
        try:
            self.clearAndType(self.email, email)
            self.clearAndType(self.password, password)
            self.continue_button.click()
        except Exception as e:
            logger.error(f"An error occurred while registering: {e}")
            raise e

    @property
    def success(self) -> bool:
        logger.info(self._driver.current_url)
        try:
            WebDriverWait(self._driver, self.WAIT_TIME // 2).until(
                EC.url_matches(Profile.urls[0])
            )
        except TimeoutException:
            return False

        return True
