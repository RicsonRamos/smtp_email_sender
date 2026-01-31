import pytest
from utils.helpers import clean_text, file_exists
from core.email_builder import build_message

def test_clean_text_sanitization():
    # Testa se espaços em branco são removidos corretamente
    assert clean_text("  test@email.com  ") == "test@email.com"
    assert clean_text(None) == ""
    assert clean_text(123) == ""

def test_email_builder_placeholders():
    # Dados fictícios para o teste
    company = "Vulcan Corp"
    receiver = "test@test.com"
    sender = "Spock"
    subject = "Saudações"
    body = "Vida longa e próspera."

    # Chamada corrigida com todos os 5 argumentos necessários
    msg = build_message(company, receiver, sender, subject, body)
    
    # Validações simples para ver se a mensagem foi construída
    assert msg['To'] == receiver
    assert msg['Subject'] == subject
    assert sender in msg.as_string()
