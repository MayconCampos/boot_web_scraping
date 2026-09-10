import logging
from boot_extracao.main import disparar_extracao
from transformacao_excel.main import disparar_ajuste
from boot_shift.main import disparar_critica

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
    arquivo_baixado = disparar_extracao()
    if not arquivo_baixado:
        raise SystemExit("Fluxo interrompido: a extração falhou.")

    arquivo_ajustado = disparar_ajuste(arquivo_baixado)
    if not arquivo_ajustado:
        raise SystemExit("Fluxo interrompido: a transformação falhou.")

    if not disparar_critica():
        raise SystemExit("Fluxo interrompido: o envio ao Shift falhou.")