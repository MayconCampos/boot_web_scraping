import logging

from .lancamento import (
    abrir_navegador,
    login,
    aba_apuracao,
    importando_critica,
    anexando_critica
)

def disparar_critica(mes_importacao, ano_importacao):
    driver = None
    try:
        driver, wait = abrir_navegador()
        login(wait)
        aba_apuracao(driver, wait)
        importando_critica(wait,mes_importacao, ano_importacao)
        anexando_critica(driver, wait)
        return True
    except Exception:
        logging.exception("Falha ao enviar o arquivo ao Shift.")
        return False
    finally:
        if driver is not None:
            driver.quit()
if __name__ == "__main__":
    disparar_critica()