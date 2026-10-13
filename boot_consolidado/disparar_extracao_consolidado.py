# Alterado pelo Codex (13/10/2026): integração dos consolidados e execução após as críticas.
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
    """Resumo: Executa o fluxo completo de extração do relatório consolidado.

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
        logging.exception("Falha durante a extração do relatório consolidado.")
        return None
    finally:
        if driver is not None:
            driver.quit()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Extrai o consolidado. Execute com python -m boot_consolidado.disparar_extracao_consolidado')
    parser.add_argument('mes', help='Nome do mês, por exemplo Outubro')
    parser.add_argument('ano', type=int)
    args = parser.parse_args()
    if not disparar_extracao_consolidado(args.mes, args.ano):
        raise SystemExit(1)
