import os
import sys
from pathlib import Path

from dotenv import load_dotenv


if getattr(sys, "frozen", False):
    pasta_configuracao = Path(sys.executable).resolve().parent
else:
    pasta_configuracao = Path(__file__).resolve().parent


load_dotenv(pasta_configuracao / ".env")


def _obter_variavel_obrigatoria(nome: str) -> str:
    valor = os.getenv(nome)
    if not valor:
        raise RuntimeError(
            f"A variável de ambiente obrigatória '{nome}' não foi definida. "
            "Configure-a no arquivo .env."
        )
    return valor


DATACG_LOGIN = _obter_variavel_obrigatoria("DATACG_LOGIN")
DATACG_PASSWORD = _obter_variavel_obrigatoria("DATACG_PASSWORD")
SHIFT_LOGIN = _obter_variavel_obrigatoria("SHIFT_LOGIN")
SHIFT_PASSWORD = _obter_variavel_obrigatoria("SHIFT_PASSWORD")
