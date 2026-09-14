import logging
from boot_extracao.main import disparar_extracao
from transformacao_excel.main import disparar_ajuste
from boot_shift.main import disparar_critica
from conf_geral import data_referencia , data_anterior

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

if __name__ == "__main__":
    for loop in range(2):
        if loop == 0:
            funcao_data = data_anterior
        else:
            funcao_data = data_referencia
            
        arquivo_baixado = disparar_extracao(funcao_data)
        
        if not arquivo_baixado:
            raise SystemExit("Fluxo interrompido: a extração falhou.")
        arquivo_ajustado = disparar_ajuste(arquivo_baixado)
        
        if not arquivo_ajustado:
            raise SystemExit("Fluxo interrompido: a transformação falhou.")
        
        if not disparar_critica(funcao_data):
            raise SystemExit("Fluxo interrompido: o envio ao Shift falhou.")