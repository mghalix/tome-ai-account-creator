"""Namespaced constants"""

from selenium.webdriver.common.by import By

URLS = {
    "login": "https://tome.app/login",
    "register": "https://tome.app/signup",
    "profile": [
        "https://tome.app/create-profile",
        "https://tome.app/verify",
    ],
    "preference": [
        "https://tome.app/customize-brand",
        "https://tome.app/upgrade",
    ],
    "workspace": [
        "https://tome.app/create-workspace",
        "https://tome.app/join-workspace",
    ],
}

LOCATORS = {
    "login": {
        "username": (By.ID, "username"),
        "password": (By.ID, "password"),
        "sign_in_button": (
            By.XPATH,
            "/html/body/main/section/div/div/div/form/div[3]/button",
        ),
    },
    "register": {
        "email": (By.ID, "email"),
        "password": (By.ID, "password"),
        "continue_button": (By.NAME, "action"),
    },
    "profile": {
        "first_name": (By.NAME, "firstName"),
        "last_name": (By.NAME, "lastName"),
        "work": (
            By.CSS_SELECTOR,
            "div.Item__StyledItem-sc-a6b0160c-0:nth-child(12)",
        ),
        "next_button": (By.XPATH, "/html/body/div[1]/div/div/div/form/button"),
        "dropdown": (
            By.CLASS_NAME,
            "InputDropdown__ButtonIconStyle-sc-e806ca2d-1",
        ),
        "verify_button": (
            By.CSS_SELECTOR,
            ".Onboarding-styles__Button-sc-da1262eb-15",
        ),
    },
    "preference": {
        "next_button": (
            By.CSS_SELECTOR,
            ".Onboarding-styles__Button-sc-da1262eb-15",
        ),
        "basic_plan": (
            By.CSS_SELECTOR,
            "div.PlanCard-styles__Container-sc-bd1aa1ef-1:nth-child(1)",
        ),
        "continue_button": (
            By.CSS_SELECTOR,
            ".TomeButton__TruncatedButtonLabelContainer-sc-398f3cf6-4",
        ),
        "dark_theme": (
            By.CSS_SELECTOR,
            "button.ButtonReset__StyledResetButton-sc-71a878e8-0:nth-child(1)",
        ),
        "light_theme": (
            By.CSS_SELECTOR,
            "button.ButtonReset__StyledResetButton-sc-71a878e8-0:nth-child(2)",
        ),
        "neptune_theme": (
            By.CSS_SELECTOR,
            "button.ButtonReset__StyledResetButton-sc-71a878e8-0:nth-child(3)",
        ),
        "creme_theme": (
            By.CSS_SELECTOR,
            "button.ButtonReset__StyledResetButton-sc-71a878e8-0:nth-child(4)",
        ),
    },
    "workspace": {
        "workspace_name": (By.CSS_SELECTOR, ".Input-sc-5f184623-0"),
        "next_button": (
            By.CSS_SELECTOR,
            ".Onboarding-styles__Button-sc-da1262eb-15",
        ),
    },
}
