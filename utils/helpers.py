import os
from typing import Optional


def garantir_pasta(caminho: str) -> None:
    os.makedirs(caminho, exist_ok=True)


def arquivo_existe(caminho: str) -> bool:
    return os.path.exists(caminho)


def limpar_texto(s: Optional[str]) -> str:
    return s.strip() if isinstance(s, str) else ""
