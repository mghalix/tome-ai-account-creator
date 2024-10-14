import logging

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.model.preference import Preference
from src.model.profile import Profile
from src.model.webpage import WebPage
from src.model.workspace import Workspace
from src.scripts.constants import LOCATORS, URLS

logger = logging.getLogger(__name__)


class Login(WebPage):
    _name = __name__.split(".")[-1]
    url: str = URLS[_name]
    USERNAME_LOCATOR = LOCATORS[_name]["username"]
    PASSWORD_LOCATOR = LOCATORS[_name]["password"]
    SIGN_IN_BUTTON_LOCATOR = LOCATORS[_name]["sign_in_button"]

    @property
    def username(self) -> WebElement:
        try:
            return WebDriverWait(self._driver, self.WAIT_TIME).until(
                EC.presence_of_element_located(self.USERNAME_LOCATOR)
            )
        except TimeoutException as e:
            logging.error("Timeout while waiting for username field")
            raise e

    @property
    def password(self) -> WebElement:
        try:
            return WebDriverWait(self._driver, self.WAIT_TIME).until(
                EC.presence_of_element_located(self.PASSWORD_LOCATOR)
            )
        except TimeoutException as e:
            logging.error("Timeout while waiting for password field")
            raise e

    @property
    def sign_in(self) -> WebElement:
        try:
            return WebDriverWait(self._driver, self.WAIT_TIME).until(
                EC.presence_of_element_located(self.SIGN_IN_BUTTON_LOCATOR)
            )
        except TimeoutException as e:
            logging.error("Timeout while waiting for sign-in button")
            raise e

    def login(self, username: str, password: str) -> None:
        try:
            self.clearAndType(self.username, username)
            self.clearAndType(self.password, password)
            self.sign_in.click()
        except Exception as e:
            logging.error(f"An error occurred while logging in: {e}")
            raise e

    @property
    def success(self) -> bool:
        next_pages: list[str] = Profile.urls + Workspace.urls + Preference.urls

        logging.info(self._driver.current_url)
        try:
            WebDriverWait(self._driver, self.WAIT_TIME // 2).until(
                lambda driver: any(EC.url_contains(page)(driver) for page in next_pages)
            )
        except TimeoutException:
            return False

        return True
