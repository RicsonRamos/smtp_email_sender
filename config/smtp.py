import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587  # TLS Port

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")

# Validation to prevent runtime crashes without clear reasons
if not SENDER_EMAIL or not APP_PASSWORD:
    raise RuntimeError(
        "SMTP Credentials not found. Please ensure SENDER_EMAIL and "
        "APP_PASSWORD are set in your .env file."
    )