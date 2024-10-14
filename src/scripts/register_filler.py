from selenium.webdriver.remote.webdriver import WebDriver

from src.model.register import Register


def fill(driver: WebDriver, register_data: list[str]) -> bool:
    register = Register(driver=driver)
    register.open()
    input("Solve captcha and press enter to continue...")
    register.register(email=register_data[0], password=register_data[1])

    status = register.success
    if status:
        print("Register successfully")
        return True

    print(f"Create profile status {status}")
    return False
