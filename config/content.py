import os

# Edit the email subject here
EMAIL_SUBJECT = "Internship Application - Criminal Law - {company}"

# Define your professional persona here
SENDER_NAME = ""

# Logic to pull body text from email.txt
def load_body_template():
    
    file_path = "templates/email.txt"
    
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        # Fallback caso o arquivo não exista
        return "Template file not found. Please create email.txt."

# This variable now automatically holds the content of email.txt
EMAIL_BODY_TEXT = load_body_template()