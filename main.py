import logging
from datetime import date
from conf_geral import data_anterior, data_referencia


def fluxo_criticas(mes, ano):
    """Resumo: Executa a extração, o tratamento e o envio das críticas ao Shift.

    Parâmetros: mes (str), nome do mês; ano (int), ano de referência.

    Retorno: Nenhum. Levanta RuntimeError se uma etapa falhar.
    """
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
    """Resumo: Executa a extração, o tratamento e o envio do consolidado ao Shift.

    Parâmetros: mes (str), nome do mês; ano (int), ano de referência.

    Retorno: Nenhum. Interrompe o fluxo se uma etapa falhar.
    """
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
    """Resumo: Processa as críticas e, no dia 20, tenta depois o consolidado do mês anterior, mesmo se as críticas falharem.

    Parâmetros: hoje (date, opcional), data da execução; executar_criticas e executar_consolidado (funções, opcionais), substituições para testes sem acesso aos sistemas.

    Retorno: Nenhum em caso de sucesso. Ao final, levanta RuntimeError com os fluxos que falharam. As críticas processam o mês anterior e o atual antes do dia 18; nos demais dias, somente o atual. Esta função depende de uma chamada externa e não agenda sua própria execução.
    """
    hoje = hoje or date.today()
    executar_criticas = executar_criticas or fluxo_criticas
    executar_consolidado = executar_consolidado or fluxo_consolidado
    periodos = []
    if hoje.day < 18:
        periodos.append(data_anterior(hoje.month, hoje.year))
    periodos.append(data_referencia(hoje.month, hoje.year))
    falhas = []

    for mes, ano in periodos:
        logging.info('Processando críticas: %s/%s', mes, ano)
        try:
            executar_criticas(mes, ano)
        except Exception:
            logging.exception('Falha nas críticas: %s/%s', mes, ano)
            falhas.append(f'Críticas {mes}/{ano}')
        else:
            logging.info('Críticas concluídas: %s/%s', mes, ano)

    if hoje.day == 20:
        mes, ano = data_anterior(hoje.month, hoje.year)
        logging.info('Processando consolidado: %s/%s', mes, ano)
        try:
            executar_consolidado(mes, ano)
        except Exception:
            logging.exception('Falha no consolidado: %s/%s', mes, ano)
            falhas.append(f'Consolidado {mes}/{ano}')
        else:
            logging.info('Consolidado concluído: %s/%s', mes, ano)
    else:
        logging.info('Consolidado não executado: a execução mensal ocorre no dia 20.')

    if falhas:
        raise RuntimeError('Execução encerrada com falhas: ' + '; '.join(falhas))
    logging.info('Todos os fluxos previstos para hoje foram concluídos.')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    try:
        executar()
    except Exception:
        logging.exception('Execução com falha. Consulte os registros antes de repetir qualquer envio.')
        raise SystemExit(1)
