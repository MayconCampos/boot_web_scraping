import logging
from boot_extracao.main import disparar_extracao
from transformacao_excel.main import disparar_ajuste
from boot_shift.main import disparar_critica
from conf_geral import data_referencia , data_anterior, data_atual

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
ano_ref, mes_ref, dia_ref = data_atual()

if __name__ == "__main__":
    if dia_ref < 16:
        for loop in range(2):
            if loop == 0:
                mes_importacao, ano_importacao = data_anterior(mes_ref,ano_ref)
            else:
                mes_importacao, ano_importacao = data_referencia(mes_ref,ano_ref)
            
            arquivo_baixado = disparar_extracao(mes_importacao, ano_importacao)
                        
            if not arquivo_baixado:
                raise SystemExit("Fluxo interrompido: a extração falhou.")
            arquivo_ajustado = disparar_ajuste(arquivo_baixado)
            
            if not arquivo_ajustado:
                raise SystemExit("Fluxo interrompido: a transformação falhou.")
            
            if not disparar_critica(mes_importacao, ano_importacao):
                raise SystemExit("Fluxo interrompido: o envio ao Shift falhou.")
    else:
        mes_importacao, ano_importacao = data_referencia(mes_ref,ano_ref)
        
        arquivo_baixado = disparar_extracao(mes_importacao, ano_importacao)
                    
        if not arquivo_baixado:
            raise SystemExit("Fluxo interrompido: a extração falhou.")
        arquivo_ajustado = disparar_ajuste(arquivo_baixado)
        
        if not arquivo_ajustado:
            raise SystemExit("Fluxo interrompido: a transformação falhou.")
        
        if not disparar_critica(mes_importacao, ano_importacao):
            raise SystemExit("Fluxo interrompido: o envio ao Shift falhou.")