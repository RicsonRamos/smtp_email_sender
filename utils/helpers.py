import os
from typing import Optional

def ensure_directory(path: str) -> None:
    """
    Ensures that a directory exists at the specified path.
    Creates it if it does not already exist.
    """
    os.makedirs(path, exist_ok=True)

def file_exists(path: str) -> bool:
    """
    Checks if a file or directory exists at the given path.
    """
    return os.path.exists(path)

def clean_text(text: Optional[str]) -> str:
    """
    Removes leading and trailing whitespace from a string.
    Returns an empty string if the input is None or not a string.
    """
    if isinstance(text, str):
        return text.strip()
    return ""
