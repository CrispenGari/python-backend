
"""
* This code was obtained on stackoverflow: https://stackoverflow.com/questions/10147455/how-to-send-an-email-with-gmail-as-provider-using-python
# SETTING UP
    - GO TO https://myaccount.google.com/security
    - MAKE SURE THAT '2-STEP VERIFICATION IS ENABLED'
    - ONCE THAT IS THERE GO TO '2-STEP VERIFICATION' THEN   APP PASSWORDS
    - GIVE YOUR APP A NAME AND GENERATE THE PASSWORD STORE IT SAFE.
# READ MORE ABOUT ENVIRONMENTAL VARIABLES HERE: https://fastapi.tiangolo.com/environment-variables/#create-and-use-env-vars
"""

import smtplib
from email.mime.text import MIMEText
import ssl

YOUR_GOOGLE_EMAIL = (
    "crispendev@gmail.com"  # The email you setup to send the email using app password
)
YOUR_GOOGLE_EMAIL_APP_PASSWORD = "bhdk sytc kkso wdey"  # The app password you generated

def send_email(subject: str, to: str, html: str):
    try:
        message = MIMEText(html, "html")
        message["Subject"] = subject
        message["From"] = YOUR_GOOGLE_EMAIL
        message["To"] = to
        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(YOUR_GOOGLE_EMAIL, YOUR_GOOGLE_EMAIL_APP_PASSWORD)
            server.sendmail(YOUR_GOOGLE_EMAIL, to, message.as_string())
    except Exception:
        return False
    return True



