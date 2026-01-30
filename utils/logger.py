import logging
from config.paths import LOG_FILE

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def log_event(message: str) -> None:
    """
    Logs an info message to both file and console.

    This function logs an info message to both the file specified in the
    configuration and the console. It is used to log events that occur
    during the execution of the email campaign process.

    Args:
        message (str): The message to be logged.
    """
    logging.info(message)

# Alias to avoid breaking other files temporarily if needed
registrar_log = log_event