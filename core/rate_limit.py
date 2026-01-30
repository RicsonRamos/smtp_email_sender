import random
import time
from datetime import date
from config.limits import DELAY_MIN, DELAY_MAX, DAILY_LIMIT
from utils.logger import log_event

class RateLimiter:
    """
    Manages sending speed and daily quotas to avoid being flagged as spam.
    """

    def __init__(self):
        """
        Initializes the RateLimiter instance.
        Keeps track of the current date and the number of emails sent today.
        """
        self._current_date = date.today()
        self._sent_today = 0

    def _reset_if_new_day(self) -> None:
        """
        Resets the counter of emails sent today if the calendar day has changed.

        This method is used internally by the RateLimiter to keep track of the
        number of emails sent each day. It will reset the counter if the
        current day is different from the previous one.

        :return: None
        """
        today = date.today()
        if today != self._current_date:
            # Reset the counter and log the event
            self._current_date = today
            self._sent_today = 0
            log_event("New day detected: Daily sending counter reset.")

    def can_send(self) -> bool:
        """
        Checks if the daily limit has been reached.

        Resets the counter if a new day is detected and then checks
        if the number of emails sent today is below the daily limit.

        :return: True if the email can be sent, False otherwise
        """
        self._reset_if_new_day()
        return self._sent_today < DAILY_LIMIT

    def register_send(self) -> None:
        """
        Increments the counter of emails sent today.

        This method is used to keep track of the number of emails sent
        today. It will reset the counter if a new day is detected and
        then increment the counter by one.

        :return: None
        """
        self._reset_if_new_day()
        # Increment the counter and log the event
        self._sent_today += 1
        log_event(f"Email sent: {self._sent_today}/{DAILY_LIMIT} emails sent today.")

    def get_random_delay(self) -> float:
        """
        Calculates a random delay between the configured DELAY_MIN and DELAY_MAX.

        The random delay is used to avoid hitting the mail server too quickly.

        :return: A random float between DELAY_MIN and DELAY_MAX
        """
        return random.uniform(DELAY_MIN, DELAY_MAX)

    def wait(self):
        """
        Executes the sleep for the random delay period.

        This method waits for a random period of time between DELAY_MIN and DELAY_MAX
        seconds before sending the next email. The purpose of this delay is to avoid hitting
        the mail server too quickly.

        :return: None
        """
        # Calculate a random delay period
        delay = self.get_random_delay()

        # Log the event and wait for the delay period
        log_event(f"Waiting for {delay:.2f} seconds before next send...")
        time.sleep(delay)

    def get_status(self) -> str:
        """
        Returns the current usage status as a string.

        The status string contains the number of emails sent today and the
        daily limit.

        :return: A string containing the current usage status
        """
        return f"""Status: {self._sent_today}/{DAILY_LIMIT} emails sent today."""
