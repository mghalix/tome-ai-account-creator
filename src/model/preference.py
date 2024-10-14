import logging
from enum import StrEnum, auto
from typing import Self, TypeAlias

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.model.webpage import WebPage
from src.scripts.constants import LOCATORS, URLS

logger = logging.getLogger(__name__)

Locator: TypeAlias = tuple[str, str]


class ColorScheme(StrEnum):
    DARK = auto()
    LIGHT = auto()
    NEPTUNE = auto()
    CREME = auto()

    @classmethod
    def parse(cls, value: str | Self) -> "ColorScheme":
        if isinstance(value, cls):
            return value

        if not isinstance(value, str):
            raise ValueError(f"Cannot convert {type(value).__name__} to a ColorScheme")

        value = value.strip().lower()

        match value:
            case "dark":
                return cls.DARK
            case "light":
                return cls.LIGHT
            case "neptune":
                return cls.NEPTUNE
            case "creme":
                return cls.CREME
            case _:
                raise ValueError(f"Invalid color scheme: {value}")


class Preference(WebPage):
    _name = __name__.split(".")[-1]
    urls: list[str] = URLS[_name]
    NEXT_BUTTON_LOCATOR = LOCATORS[_name]["next_button"]
    BASIC_PLAN_LOCATOR = LOCATORS[_name]["basic_plan"]
    CONTINUE_BUTTON_LOCATOR = LOCATORS[_name]["continue_button"]

    _themes: dict[ColorScheme, Locator] = {
        ColorScheme.DARK: LOCATORS[_name]["dark_theme"],
        ColorScheme.LIGHT: LOCATORS[_name]["light_theme"],
        ColorScheme.NEPTUNE: LOCATORS[_name]["neptune_theme"],
        ColorScheme.CREME: LOCATORS[_name]["creme_theme"],
    }

    def _get_theme_locator(self, theme: str | None = None) -> Locator:
        if theme is None:
            return self._default_theme

        try:
            parsed_theme = ColorScheme.parse(theme)
        except:
            return self._default_theme

        return self._themes.get(parsed_theme, self._default_theme)

    @property
    def _default_theme(self) -> Locator:
        return self._themes[ColorScheme.DARK]

    def _theme_element(self, theme_name: str | None) -> WebElement:
        try:
            return WebDriverWait(self._driver, self.WAIT_TIME).until(
                EC.element_to_be_clickable(self._get_theme_locator(theme_name))
            )
        except TimeoutException as e:
            logging.error(f"Timeout while waiting for theme: {theme_name}")
            raise e

    @property
    def next(self) -> WebElement:
        try:
            return WebDriverWait(self._driver, self.WAIT_TIME).until(
                EC.element_to_be_clickable(self.NEXT_BUTTON_LOCATOR)
            )
        except TimeoutException as e:
            logging.error("Timeout while waiting for next button")
            raise e

    def pick_theme(self, theme: str | None = None) -> None:
        try:
            self._theme_element(theme).click()
            self.next.click()
        except Exception as e:
            logging.error(f"An error occurred while picking theme: {e}")
            raise e

    @property
    def basic_plan(self) -> WebElement:
        try:
            return WebDriverWait(self._driver, self.WAIT_TIME).until(
                EC.presence_of_element_located(self.BASIC_PLAN_LOCATOR)
            )
        except TimeoutException as e:
            logging.error("Timeout while waiting for basic plan")
            raise e

    @property
    def continue_button(self) -> WebElement:
        try:
            return WebDriverWait(self._driver, self.WAIT_TIME).until(
                EC.presence_of_element_located(self.CONTINUE_BUTTON_LOCATOR)
            )
        except TimeoutException as e:
            logging.error("Timeout while waiting for continue button")
            raise e

    def pick_free_plan(self) -> None:
        try:
            self.basic_plan.click()
            self.continue_button.click()
            WebDriverWait(self._driver, self.WAIT_TIME).until(
                EC.url_changes(self._driver.current_url)
            )
        except Exception as e:
            logging.error(f"An error occurred while picking free plan: {e}")
            raise e

    @property
    def success(self) -> bool:
        try:
            WebDriverWait(self._driver, self.WAIT_TIME // 2).until(
                EC.url_changes(self.urls[1])
            )
        except TimeoutException:
            return False

        return True

    @property
    def at_theme_page(self) -> bool:
        try:
            WebDriverWait(self._driver, self.WAIT_TIME).until(
                EC.url_to_be(self.urls[0])
            )
        except TimeoutException:
            return False
        return True

    @property
    def at_plan_page(self) -> bool:
        try:
            WebDriverWait(self._driver, self.WAIT_TIME).until(
                EC.url_to_be(self.urls[1])
            )
        except TimeoutException:
            return False
        return True
