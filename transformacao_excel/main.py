from .arquivo_critica import (
    buscar_ultima_critica
)

from .df_ajustada import (
    ajuste_base,
    regras_negocio,
    exportando_excel
)

def disparar_ajuste(caminho=None):
    try:
        if caminho is None:
            caminho, status = buscar_ultima_critica()
            if not status:
                return False
        df_reordenada = ajuste_base(caminho)
        df_reordenada = regras_negocio(df_reordenada)
        return exportando_excel(df_reordenada)
    except Exception as erro:
        print(f"Falha ao transformar o arquivo {caminho}: {erro}")
        return False

if __name__ == "__main__":
    disparar_ajuste()
