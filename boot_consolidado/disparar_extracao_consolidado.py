import logging
from .extracao_consolidado import (
    abrir_navegado,
    login_sistema,
    perfis_acesso,
    gerando_relatorio,
    exportando_computador,
    aguardar_novo_download
)

def disparar_extracao_consolidado(mes_importacao, ano_importacao):
    """Resumo: Executa o fluxo completo de extração do relatório de críticas.

    Parâmetros: mes_importacao (str), mês a extrair; ano_importacao (int), ano a extrair.

    Retorno: Caminho do arquivo baixado ou None quando a extração falha.
    """
    driver = None
    try:
        driver, wait = abrir_navegado()
        login_sistema(wait)
        perfis_acesso(wait)
        gerando_relatorio(wait,mes_importacao, ano_importacao)
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

# if __name__ == "__main__":
#     # Permite executar este módulo isoladamente durante testes manuais.
#     disparar_extracao_consolidado()

#teste
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s"
    )

    mes_importacao = "Setembro"
    ano_importacao = 2026

    arquivo_baixado = disparar_extracao_consolidado(
        mes_importacao,
        ano_importacao
    )

    if arquivo_baixado:
        print(f"Teste concluído. Arquivo baixado: {arquivo_baixado}")
    else:
        print("Teste falhou. Verifique os logs acima.")