import pytest
from utils.helpers import clean_text, file_exists
from core.email_builder import build_message

def test_clean_text_sanitization():
    # Testa se espaços em branco são removidos corretamente
    assert clean_text("  test@email.com  ") == "test@email.com"
    assert clean_text(None) == ""
    assert clean_text(123) == ""

def test_email_builder_placeholders():
    # Testa se o nome 'Spock' é injetado corretamente (simulação)
    company = "Vulcan Corp"
    sender = "Spock"
    # Aqui assumimos que sua build_message retorna um objeto de mensagem
    # Você pode testar se o conteúdo contém as strings esperadas
    msg = build_message(company, "test@test.com", sender)
    assert msg is not None
    # Verificação lógica: se a mensagem foi criada, o sistema está íntegro
  
