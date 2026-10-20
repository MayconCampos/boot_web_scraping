import logging

from .lancamento import (
    abrir_navegador,
    login,
    aba_apuracao,
    importando_critica,
    anexando_critica
)

def disparar_critica(mes_importacao, ano_importacao, caminho_arquivo):
    """Resumo: Executa o envio da crítica processada ao sistema Shift.

    Parâmetros: mes_importacao (str), mês; ano_importacao (int), ano; caminho_arquivo (str ou Path), Excel gerado nesta execução.

    Retorno: True após a confirmação de sucesso; False em falhas de envio. Arquivo inexistente gera erro antes de abrir o navegador.
    
    obs: Esses dados de criticas são guardados na tabela "SHIFT.Producao.HistoricoCriticas"
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
