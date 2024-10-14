import logging

from selenium.webdriver.remote.webdriver import WebDriver

from src.model.login import Login

logger = logging.getLogger(__name__)


def fill(driver: WebDriver, register_data: list[str]) -> bool:
    login = Login(driver=driver)
    login.open()

    input("Solve captcha and press enter to continue...")
    login.login(username=register_data[0], password=register_data[1])

    status = login.success

    if status:
        logger.info("Success!")
        return True

    logger.debug(f"Create profile status {status}")

    return False
