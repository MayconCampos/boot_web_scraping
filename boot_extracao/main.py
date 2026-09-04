import logging
from .extracao import (
    abrir_navegador,
    login_sistema,
    perfis_acesso,
    gerando_relatorio,
    exportando_computador,
    aguardar_novo_download
)

def disparar_extracao():
    driver = None
    try:
        driver, wait = abrir_navegador()
        login_sistema(wait)
        perfis_acesso(wait)
        gerando_relatorio(wait)
        arquivos_antes = exportando_computador(driver, wait)
        arquivo_baixado = aguardar_novo_download(arquivos_antes)
        logging.info("Download concluído: %s", arquivo_baixado)
        return arquivo_baixado
    except Exception:
        logging.exception("Falha durante a extração do relatório de críticas.")
        return None
    finally:
        if driver is not None:
            driver.quit()

if __name__ == "__main__":
    disparar_extracao()
