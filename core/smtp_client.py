import smtplib
from smtplib import SMTPAuthenticationError
from config.smtp import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, APP_PASSWORD
from utils.logger import registrar_log

from typing import Union
from smtplib import SMTP, SMTPAuthenticationError, SMTPException


def connect() -> Union[SMTP, None]:
    """
    Connect to the SMTP server and authenticate the email.
    Return the smtplib.SMTP object if successful.
    Raises SMTPAuthenticationError if authentication fails.
    Raises SMTPException if any other error occurs.
    """
    try:
        # Creating the object with timeout
        server: SMTP = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=60)
        
        # Start TLS encryption
        # This is required for most SMTP servers
        server.starttls()
        
        # Login
        # Use the email address and App Password
        server.login(SENDER_EMAIL, APP_PASSWORD)

        registrar_log("SMTP connected and authenticated")
        return server

    except SMTPAuthenticationError:
        # Authentication failed
        # Check the email address and App Password
        registrar_log("Authentication failed: Check the email or App Password.")
        raise
    except SMTPException as e:
        # Unexpected error
        # Log the error and raise it
        registrar_log(f"Unexpected error connecting to SMTP: {e}")
        raise

def disconnect(server):
    """
    Disconnect from the SMTP server.
    If the server is given, call quit() to disconnect cleanly.
    If an error occurs, call close() to force the connection closed.
    """
    if server:
        try:
            # Try to disconnect cleanly
            server.quit()
        except Exception:
            pass
        finally:
            # Force the connection closed
            server.close()
            registrar_log("SMTP connection closed")
