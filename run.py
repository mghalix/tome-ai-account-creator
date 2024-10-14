import logging
import os
from contextlib import contextmanager

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options

import src.scripts.login_filler as login_filler
import src.scripts.preference_filler as preference_filler
import src.scripts.profile_filler as profile_filler
import src.scripts.register_filler as register_filler
import src.scripts.workspace_filler as workspace_filler
from src.model.excel import Excel

logging.basicConfig(level=logging.INFO)
logging.getLogger("src").setLevel(logging.DEBUG)


@contextmanager
def init_driver():
    options = Options()
    options.binary_location = "../geckodriver.exe"

    driver = webdriver.Firefox(options=options)
    try:
        yield driver
    finally:
        driver.quit()


def main() -> None:
    sheet_path = os.path.abspath("src/resources/tome-fake-accs.xlsx")

    register_data = Excel(
        sheet_path,
        "RegisterInfo",
    ).values_list

    profile_data = Excel(
        sheet_path,
        "Profile",
    ).values_list

    workspace_data = Excel(
        sheet_path,
        "Workspace",
    ).values_list

    preference_data = Excel(
        sheet_path,
        "Preference",
    ).values_list

    def process_data(data, profile_data, workspace_data, preference_data):
        with init_driver() as driver:
            try:
                result = register_filler.fill(driver, data)

                if not result:
                    result = login_filler.fill(driver, data)

                if not result:
                    return

                profile_filler.fill(driver, profile_data)
                workspace_filler.fill(driver, workspace_data)
                preference_filler.fill(driver, preference_data)
            except Exception as e:
                print(f"An error occurred: {e}")

    for data in register_data[7:]:
        process_data(
            data,
            profile_data,
            workspace_data,
            preference_data,
        )


if __name__ == "__main__":
    main()
