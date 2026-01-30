from pathlib import Path
from email.message import EmailMessage
from config.smtp import SENDER_EMAIL
from config.paths import ATTACHMENTS_DIR  # Importando a pasta de anexos
from utils.logger import log_event
from config.content import EMAIL_SUBJECT, EMAIL_BODY_TEXT

# Absolute paths baseados no que você definiu
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_TXT_PATH = BASE_DIR / "templates" / "email.txt"
TEMPLATE_HTML_PATH = BASE_DIR / "templates" / "email.html"

def build_message(company_name, target_email, sender_name):
    """
    Builds a multipart email message with a plaintext body, an HTML alternative,
    and multiple PDF attachments.
    
    Parameters:
    company_name (str): The name of the company to which we are applying.
    target_email (str): The email address to which we are sending the email.
    sender_name (str): The name of the sender (i.e., the user running the script).
    
    Returns:
    msg (EmailMessage): The constructed email message, or None if there is an error.
    """
    msg = EmailMessage()
    
    # 1. Assunto e Headers
    msg['Subject'] = EMAIL_SUBJECT.format(empresa=company_name)
    msg['From'] = f"{sender_name} <{SENDER_EMAIL}>"
    msg['To'] = target_email

    # 2. Preenchimento do Conteúdo
    # Primeiro formatamos o texto base
    texto_final = EMAIL_BODY_TEXT.format(nome=sender_name, empresa=company_name)

    try:
        with open(TEMPLATE_HTML_PATH, "r", encoding="utf-8") as f:
            html_template = f.read()
            # Inserimos o texto formatado dentro da "moldura" HTML
            html_final = html_template.format(corpo=texto_final)
        
        msg.set_content(texto_final)
        msg.add_alternative(html_final, subtype='html')
    except Exception as e:
        log_event(f" Erro ao processar templates: {e}")
        return None

    # 3. Anexos (Múltiplos)
    pdf_files = list(ATTACHMENTS_DIR.glob("*.pdf"))
    for pdf_path in pdf_files:
        with open(pdf_path, "rb") as f:
            msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=pdf_path.name)
            
    return msg