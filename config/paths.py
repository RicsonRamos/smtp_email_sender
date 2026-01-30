from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

CONTACTS_CSV = BASE_DIR / "data" / "contacts.csv"
FINISHED_CSV = BASE_DIR / "data" / "finished.csv"
LOG_FILE = BASE_DIR / "logs" / "emails.log"  # <--- O nome deve ser este!
ATTACHMENT_PATH = BASE_DIR / "attachments"