from abc import ABC
from typing import Self

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class WebPage(ABC):
    url: str
    _driver: WebDriver
    #* Increase this value if you have a slow internet connection
    WAIT_TIME = 7

    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver

    def open(self) -> Self:
        self._driver.get(self.url)
        return self

    def close(self) -> Self:
        self._driver.close()
        return self

    def clearAndType(self, element: WebElement, text: str) -> None:
        element.clear()
        element.send_keys(text)

    @classmethod
    def class_name(cls) -> str:
        return cls.__name__
