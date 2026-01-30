import os
import csv
from datetime import datetime
from pathlib import Path
from typing import List, Dict
from config.paths import CONTACTS_CSV, FINISHED_CSV
from utils.logger import log_event

# Define internal fields for consistency
FIELDS = ["company", "email"]

def load_contacts() -> List[Dict[str, str]]:
    """
    Reads the contacts CSV and returns a list of valid company/email dictionaries.
    
    This function will return an empty list if the contacts CSV does not exist.
    """
    if not CONTACTS_CSV.exists():
        log_event(f"❌ Contacts CSV not found: {CONTACTS_CSV}")
        return []

    contacts = []
    try:
        with open(CONTACTS_CSV, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            # Use a list comprehension to create the list of contacts
            contacts = [{"company": row.get("company", "").strip(), "email": row.get("email", "").strip()} 
                      for row in reader if row.get("company") and "@" in row.get("email", "")]
    except Exception as e:
        # Log any errors that occur while reading the contacts CSV
        log_event(f"❌ Error reading contacts: {e}")
        
    return contacts

def overwrite_contacts(contacts: List[Dict[str, str]]):
    """
    Safely overwrites the contacts file using a temporary file.

    This function writes the contacts list to a temporary file, and then
    atomically replaces the original file with the temporary file. This
    ensures that the data is not lost if an error occurs during the
    write process.
    """
    temp_file = CONTACTS_CSV.with_suffix(".tmp")

    try:
        # Use a buffer to write the contacts list to a temporary file
        with open(temp_file, mode="w", newline="", encoding="utf-8", buffering=2**16) as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(contacts)

        # Atomic replace to prevent data loss
        os.replace(temp_file, CONTACTS_CSV)
    except Exception as e:
        # Log any errors that occur during the write process
        log_event(f"❌ Failed to update contacts list: {e}")

def remove_contact(company: str, email: str):
    """
    Removes a specific contact from the main list after processing.

    This function is used to remove a contact from the main list
    after it has been processed. It is typically used after
    an email has been sent to mark the contact as finished.

    Args:
        company (str): The company name of the contact.
        email (str): The email address of the contact.

    Returns:
        None
    """
    contacts_path = CONTACTS_CSV
    contacts = []
    try:
        with open(contacts_path, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not (row["company"] == company and row["email"] == email):
                    contacts.append(row)

    except Exception as e:
        log_event(f"❌ Error reading contacts: {e}")
        
    overwrite_contacts(contacts)

def save_finished_contact(company: str, email: str, status: str, error: str = ""):
    """
    Logs the result of an email attempt into a 'finished' CSV for auditing.

    This function logs the result of an email attempt into a 'finished' CSV file.
    The CSV file contains the company name, email address, status of the email
    attempt, the date and time the email was sent, and any error messages.

    Args:
        company (str): The company name of the contact.
        email (str): The email address of the contact.
        status (str): The status of the email attempt (e.g. "sent", "error").
        error (str, optional): The error message associated with the email attempt.
            Defaults to an empty string.

    Returns:
        None
    """
    try:
        with open(FINISHED_CSV, mode="a", newline="", encoding="utf-8", buffering=2**16) as f:
            writer = csv.writer(f, lineterminator="\n")
            if not FINISHED_CSV.exists():
                writer.writerow([
                    "company",
                    "email",
                    "status",
                    "sent_at",
                    "error"
                ])

            writer.writerow([
                company,
                email,
                status,
                datetime.now().isoformat(),
                error
            ])

        log_msg = f"{status} → {company} ({email})"
        if error:
            log_msg += f" | ERROR: {error}"
        log_event(log_msg)
        
    except Exception as e:
        # Log any critical errors that occur while saving the finished log
        log_event(f"❌ Critical error saving finished log: {e}")
