import random
import time
from typing import Callable, Optional
from utils.logger import log_event

def calculate_exponential_backoff(
    attempt: int,
    base_delay: int = 10,
    max_delay: int = 300,
    jitter_ratio: float = 0.3
) -> float:
    """
    Calculates wait time using exponential backoff: base * 2^(attempt-1).
    Includes 'jitter' to randomize the delay and prevent synchronized retries.
    """
    if attempt < 1:
        # Ensure attempt is at least 1 to avoid division by zero
        attempt = 1

    # Exponential calculation: 10s, 20s, 40s, 80s... up to max_delay
    delay = min(base_delay * (2 ** (attempt - 1)), max_delay)

    # Adding jitter (random noise) to prevent synchronized retries
    jitter = random.uniform(0, delay * jitter_ratio) if delay > 0 else 0
    """
    Randomly adds noise to the delay to prevent synchronized retries.
    """
    return float(delay + jitter)

def wait_for_retry(
    attempt: int,
    base_delay: int = 10,
    max_delay: int = 300,
    jitter_ratio: float = 0.3,
    on_wait_callback: Optional[Callable[[float], None]] = None
) -> None:
    """
    Executes the sleep period based on the calculated backoff.

    This function is used to implement retry logic with an exponential backoff
    strategy. The time to wait before retrying is calculated based on the
    number of attempts, with a base delay that doubles for each attempt.

    The function also allows for a jitter ratio to be specified, which will
    randomly add noise to the delay to prevent synchronized retries.

    Args:
        attempt (int): The number of attempts made so far.
        base_delay (int, optional): The base delay for the exponential
            backoff. Defaults to 10.
        max_delay (int, optional): The maximum delay allowed. Defaults to 300.
        jitter_ratio (float, optional): The jitter ratio to use when adding
            noise to the delay. Defaults to 0.3.
        on_wait_callback (Optional[Callable[[float], None]], optional): A callback
            function to be called before sleeping. The function should take a single
            float argument, which is the time to wait in seconds. Defaults to None.
    """
    wait_time = calculate_exponential_backoff(
        attempt, 
        base_delay=base_delay, 
        max_delay=max_delay, 
        jitter_ratio=jitter_ratio
    )

    if callable(on_wait_callback):
        on_wait_callback(wait_time)
    else:
        # Log the event with the wait time
        log_event(f"🔄 Retry attempt {attempt}: Waiting {wait_time:.2f}s before next try.")

    # Sleep for the calculated time
    time.sleep(wait_time)
