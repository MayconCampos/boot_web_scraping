# Alterado pelo Codex (13/10/2026): integração dos consolidados e execução após as críticas.
import logging
from datetime import date
from conf_geral import data_anterior, data_referencia


def fluxo_criticas(mes, ano):
    from boot_extracao.disparar_extracao import disparar_extracao
    from Ajuste_base_critica.disparar_excel import disparar_ajuste
    from boot_shift.disparar_shift import disparar_critica
    arquivo = disparar_extracao(mes, ano)
    if not arquivo:
        raise RuntimeError('Críticas: a extração falhou.')
    planilha = disparar_ajuste(arquivo)
    if not planilha:
        raise RuntimeError('Críticas: a transformação falhou.')
    if not disparar_critica(mes, ano, planilha):
        raise RuntimeError('Críticas: o envio ao Shift falhou.')


def fluxo_consolidado(mes, ano):
    from boot_consolidado.disparar_extracao_consolidado import disparar_extracao_consolidado
    from Ajuste_base_consolidado.df_consolidado import disparar_ajuste_consolidado
    from boot_shift_consolidado.disparar_shift_consolidado import disparar_critica_consolidado
    arquivo = disparar_extracao_consolidado(mes, ano)
    if not arquivo:
        raise RuntimeError('Consolidado: a extração falhou.')
    planilha = disparar_ajuste_consolidado(arquivo)
    if not planilha:
        raise RuntimeError('Consolidado: a transformação falhou.')
    if not disparar_critica_consolidado(mes, ano, planilha):
        raise RuntimeError('Consolidado: o envio ao Shift falhou.')


def executar(hoje=None, executar_criticas=None, executar_consolidado=None):
    hoje = hoje or date.today()
    executar_criticas = executar_criticas or fluxo_criticas
    executar_consolidado = executar_consolidado or fluxo_consolidado
    periodos = []
    if hoje.day < 18:
        periodos.append(data_anterior(hoje.month, hoje.year))
    periodos.append(data_referencia(hoje.month, hoje.year))

    for mes, ano in periodos:
        logging.info('Processando críticas: %s/%s', mes, ano)
        executar_criticas(mes, ano)

    # Alterado pelo Codex: dia 20, depois de todas as críticas, usa os mesmos períodos.
    # A chamada normal de main.py continua sendo a entrada da automação.
    if hoje.day == 20:
        for mes, ano in periodos:
            logging.info('Processando consolidado: %s/%s', mes, ano)
            executar_consolidado(mes, ano)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    try:
        executar()
    except Exception:
        logging.exception('Fluxo interrompido. Verifique a etapa antes de repetir o envio.')
        raise SystemExit(1)
