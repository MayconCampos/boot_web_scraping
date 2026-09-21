import logging
from boot_extracao.disparar_extracao import disparar_extracao
from Ajuste_base_critica.disparar_excel import disparar_ajuste
from boot_shift.disparar_shift import disparar_critica
from conf_geral import data_referencia , data_anterior, data_atual
\
# Configura o registro de eventos e obtém a data que define o período de processamento.
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
ano_ref, mes_ref, dia_ref = data_atual()

if __name__ == "__main__":
    # Processa dois períodos antes do dia de corte e apenas o período atual nos demais dias.
    if dia_ref < 18:
        for loop in range(2):
            # Define o período correspondente à execução atual.
            if loop == 0:
                mes_importacao, ano_importacao = data_anterior(mes_ref,ano_ref)
            else:
                mes_importacao, ano_importacao = data_referencia(mes_ref,ano_ref)

            # Extrai, transforma e envia o arquivo para o período selecionado.
            arquivo_baixado = disparar_extracao(mes_importacao, ano_importacao)

            if not arquivo_baixado:
                raise SystemExit("Fluxo interrompido: a extração falhou.")
            arquivo_ajustado = disparar_ajuste(arquivo_baixado)

            if not arquivo_ajustado:
                raise SystemExit("Fluxo interrompido: a transformação falhou.")

            if not disparar_critica(mes_importacao, ano_importacao):
                raise SystemExit("Fluxo interrompido: o envio ao Shift falhou.")
    else:
        # Define e processa somente o período de referência atual.
        mes_importacao, ano_importacao = data_referencia(mes_ref,ano_ref)

        arquivo_baixado = disparar_extracao(mes_importacao, ano_importacao)

        if not arquivo_baixado:
            raise SystemExit("Fluxo interrompido: a extração falhou.")
        arquivo_ajustado = disparar_ajuste(arquivo_baixado)

        if not arquivo_ajustado:
            raise SystemExit("Fluxo interrompido: a transformação falhou.")

        if not disparar_critica(mes_importacao, ano_importacao):
            raise SystemExit("Fluxo interrompido: o envio ao Shift falhou.")
