import imaplib
import quopri
import re
from datetime import datetime, timedelta
import logging

import requests

logger = logging.getLogger(__name__)

def verify_email(email: str, password: str) -> bool:
    # connect to the email server
    mail = imaplib.IMAP4_SSL("imap.gmail.com")

    # authenticate
    try:
        logger.info("Attempting to login to email...")
        mail.login(user=email, password=password)
        logger.info("Successfully logged in to email.")
    except imaplib.IMAP4.error:
        # print("Email login failed.")
        print(
            "An error occurred while logging in to your email. Please check "
            "your credentials or network connection."
        )
        return False

    mail.select("inbox")

    data_ten_minutes_ago = datetime.now() - timedelta(minutes=10)
    date_str = data_ten_minutes_ago.strftime("%d-%b-%Y")
    _, msg_ids = mail.uid(
        "search",
        None,  # type: ignore
        # f'(FROM "Tome" SUBJECT "Verify your email address SINCE {date_str}")',
        f'(FROM "Tome" SUBJECT "Verify your email address")',
    )

    msg_id_list = msg_ids[0].split()

    if not msg_id_list:
        print("No messages found.")
        return False

    latest_email_id = msg_id_list[-1]

    # fetch the email body (RFC822) for the given ID
    _, email_data = mail.uid("fetch", latest_email_id, "(BODY.PEEK[TEXT])")
    raw_email = email_data[0][1].decode("utf-8")

    # find the verfication link
    decoded_email = decoded_email = quopri.decodestring(raw_email).decode()
    match = re.search(
        r'(https://auth\.tome\.app/u/email-verification\?ticket=[^\s"#]+)',
        decoded_email,
    )

    if match is None:
        print("No link found.")
        return False

    verification_link = match.group(0).strip("<>")

    response = requests.get(verification_link)

    if response.status_code != 200:
        print("Error verifying email.")
        print(response.text)
        return False

    print("Email verified successfully.")
    return True
