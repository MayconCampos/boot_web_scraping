




from datetime import date

# Mapeia o número do mês para seu nome usado nas telas dos sistemas.
meses = {
        1:"Janeiro",
        2:"Fevereiro",
        3:"Março",
        4:"Abril",
        5:"Maio",
        6:"Junho",
        7:"Julho",
        8:"Agosto",
        9:"Setembro",
        10:"Outubro",
        11:"Novembro",
        12:"Dezembro"
        }

def data_atual():
    """Resumo: Obtém a data corrente para controlar o processamento.

    Parâmetros: Nenhum.

    Retorno: Tupla com ano, mês e dia atuais.
    """
    data_base = date.today()
    mes_ref = data_base.month
    ano_ref = data_base.year
    dia_ref = data_base.day
    return ano_ref, mes_ref, dia_ref

def data_referencia(mes_ref, ano_ref):
    """Resumo: Converte o período de referência para o formato de importação.

    Parâmetros: mes_ref (int), número do mês; ano_ref (int), ano de referência.

    Retorno: Tupla com nome do mês e ano de importação.
    """
    mes_importacao = meses[mes_ref]
    ano_importacao = ano_ref
    return mes_importacao, ano_importacao

def data_anterior(mes_ref, ano_ref):
    """Resumo: Calcula o período imediatamente anterior ao período informado.

    Parâmetros: mes_ref (int), número do mês; ano_ref (int), ano de referência.

    Retorno: Tupla com nome do mês anterior e seu respectivo ano.
    """
    mes_atual = mes_ref
    ano_atual = ano_ref

    if mes_atual == 1:
        mes_ref = 12
        mes_importacao = meses[mes_ref]
        ano_importacao = ano_atual - 1
        return mes_importacao, ano_importacao

    mes_ref = mes_atual - 1
    mes_importacao = meses[mes_ref]
    ano_importacao = ano_atual
    return mes_importacao, ano_importacao
