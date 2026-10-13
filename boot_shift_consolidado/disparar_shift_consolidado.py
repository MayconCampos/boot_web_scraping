# Alterado pelo Codex (13/10/2026): integração dos consolidados e execução após as críticas.
import logging

from .lancamento_consolidado import (
    abrir_navegador,
    login,
    aba_apuracao,
    importando_critica,
    anexando_critica
)

def disparar_critica_consolidado(mes_importacao, ano_importacao, caminho_arquivo):
    """Resumo: Executa o envio da crítica processada ao sistema Shift.

    Parâmetros: mes_importacao (str), mês da crítica; ano_importacao (int), ano da crítica.

    Retorno: True quando o envio termina com sucesso; False em caso de falha.
    """
    from pathlib import Path
    caminho_arquivo = Path(caminho_arquivo).resolve(strict=True)
    driver = None
    try:
        driver, wait = abrir_navegador()
        login(wait)
        aba_apuracao(driver, wait)
        importando_critica(wait,mes_importacao, ano_importacao)
        anexando_critica(driver, wait, caminho_arquivo)
        return True
    except Exception:
        logging.exception("Falha ao enviar o arquivo ao Shift.")
        return False
    finally:
        if driver is not None:
            driver.quit()
            
