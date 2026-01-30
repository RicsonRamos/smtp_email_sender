import os
from pathlib import Path
from email.message import EmailMessage
from mimetypes import guess_type
from config.smtp import SENDER_EMAIL
from config.paths import ATTACHMENTS_PATH  # Importando a pasta de anexos
from utils.logger import log_event
from config.content import EMAIL_SUBJECT, EMAIL_BODY_TEXT

# Absolute paths baseados no que você definiu
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_TXT_PATH = BASE_DIR / "templates" / "email.txt"
TEMPLATE_HTML_PATH = BASE_DIR / "templates" / "email.html"

def build_message(company, target_email, sender_name, subject, body):
    """
    Constructs the email with dynamic content and multiple attachments.
    """
    try:
        msg = EmailMessage()
        
        # 1. Replace placeholders in Subject and Body
        # We use .replace() for safety if the user didn't use {} correctly
        final_subject = subject.replace("{company}", company).replace("{sender_name}", sender_name)
        final_body = body.replace("{company}", company).replace("{sender_name}", sender_name)
        
        msg['Subject'] = final_subject
        msg['From'] = f"{sender_name} <{os.getenv('SENDER_EMAIL')}>"
        msg['To'] = target_email
        msg.set_content(final_body)

        # 2. Attach every file in the attachments/ folder
        attach_dir = "attachments"
        if os.path.exists(attach_dir):
            for filename in os.listdir(attach_dir):
                file_path = os.path.join(attach_dir, filename)
                
                if os.path.isfile(file_path):
                    content_type, _ = guess_type(file_path)
                    if content_type is None:
                        content_type = 'application/octet-stream'
                    
                    maintype, subtype = content_type.split('/', 1)
                    
                    with open(file_path, 'rb') as f:
                        msg.add_attachment(
                            f.read(),
                            maintype=maintype,
                            subtype=subtype,
                            filename=filename
                        )
        return msg
    except Exception as e:
        # Se der erro aqui, o runner vai saber o motivo real
        print(f"Error building email: {e}")
        return None