import logging

from selenium.webdriver.remote.webdriver import WebDriver

from src.model.profile import Profile
from src.scripts.email_verifier import verify_email

logger = logging.getLogger(__name__)


def fill(driver: WebDriver, profile_data: list[str]) -> None:
    profile = Profile(driver=driver)

    if driver.current_url not in profile.urls:
        logger.debug("Not at profile page")
        return

    logger.debug("At profile page")
    if profile.at_profile_page:
        logger.debug("Entered profile page")
        profile.create_profile(
            first_name=profile_data[0][0], last_name=profile_data[0][1]
        )

    logger.debug("Attempting to verify profile...")
    if profile.at_verify_page:
        logger.debug("Verifying email....")
        manual_verify(profile)
        # FIXME - the auto verify method is not working (probably picks and )
        #old verification email instead of the latest
        # while not profile.verify_success:
        #     if not auto_verify(profile):
        #         logger.warning("Failed to verify email")
        #         print("Would you like to manually verify your email? (y/n)")
        #         manual = input("> ")
        #         if manual.lower() in ["y", "yes", "ye", "yep", "yeah"]:
        #             manual_verify(profile)
        #         else:
        #             auto_verify(profile)

    logger.info(f"Profile status: {profile.success}")


def manual_verify(profile: Profile) -> None:
    query: str = (
        "https://mail.google.com/mail/u/1/#advanced-search/"
        "subject=Verify&subset=all&has=Tome+your+email+address&within=1d"
        "&sizeoperator=s_sl&sizeunit=s_smb&query=from%3A+Tome+subject"
        "%3AVerify+your+email+address"
    )

    while True:
        print(f"Click here to verify: {query}")
        verified = input("Have you verified your email? (y/n)\n> ")
        match verified.lower():
            case "y" | "yes" | "ye" | "yep" | "yeah":
                profile.verify()
                if not profile.verify_success:
                    logger.warning(
                        "Please go to your email and verify before " "continuing."
                    )
                    continue

                print("Success!")
                break
            case "n":
                print("Please verify your email and try again.")
            case _:
                print("Invalid input.")


def auto_verify(profile: Profile) -> bool:
    EMAIL = "mghali2002@gmail.com"
    PASSWORD = "yrrl ciaa uuug jmef"
    status = verify_email(EMAIL, PASSWORD)
    if not status:
        return False

    profile.verify()
    return True
