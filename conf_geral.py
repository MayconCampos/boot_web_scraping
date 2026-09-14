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

def data_referencia(maiusculo = False):
    data_atual = date.today()
    mes_ref = data_atual.month

    mes_importacao = meses[mes_ref]
    ano_importacao = data_atual.year

    if maiusculo:
        mes_importacao = meses[mes_ref].upper()
        return mes_importacao, ano_importacao
    
    return mes_importacao, ano_importacao

def data_anterior(maiusuclo = False):
    data_atual = date.today()
    mes_ref = data_atual.month
    ano_importacao = data_atual.year
       
    mes_anterior = mes_ref - 1
    mes_importacao = meses[mes_anterior]
    
    if maiusuclo:
        mes_importacao = meses[mes_anterior].upper()
        return mes_importacao, ano_importacao
    
    return mes_importacao, ano_importacao