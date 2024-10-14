import logging

from selenium.webdriver.remote.webdriver import WebDriver

from src.model.workspace import Workspace

logger = logging.getLogger(__name__)


def fill(driver: WebDriver, workspace_data: list[str]) -> None:
    workspace = Workspace(driver=driver)

    if driver.current_url not in workspace.urls:
        logger.debug("Not at workspace page")
        return

    workspace.create_workspace(workspace_name=workspace_data[0])
    logging.info(f"Workspace status: {workspace.success}")
