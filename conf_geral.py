# # Lógica do código a partir de agora:

# # ele vai pegar o mês atual e vai mandar para o boot_extrador e para o boot shift
# # como vai ser um modulo a parti tenho que deixar junto com  a raiz "main" principal.

from datetime import date

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
    data_base = date.today()
    mes_ref = data_base.month
    ano_ref = data_base.year
    dia_ref = data_base.day
    return ano_ref, mes_ref, dia_ref

def data_referencia(mes_ref, ano_ref):
    mes_importacao = meses[mes_ref]
    ano_importacao = ano_ref 
    return mes_importacao, ano_importacao

def data_anterior(mes_ref, ano_ref):
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