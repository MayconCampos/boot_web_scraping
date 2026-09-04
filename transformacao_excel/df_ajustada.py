import pandas as pd

def ajuste_base(caminho):
    df_critica_sge_pura = pd.read_csv(caminho, sep=',', dtype='str')
    
    df_renomeada = df_critica_sge_pura.rename(
        columns={
            "TIPO_ERRO" : "Tipo de Erro",
            "TIPO_REGISTRO" : "Tipo de Registro",
            "NR_LINHA" : "Número da Linha",
            "codigo_erro_individual":"Código do Erro",
            "CONTEUDO_DO_CAMPO" : "Conteúdo do Campo",
            "IMPEDITIVO?" : "Impeditivo?",
            "DESC_ERRO" : "Detalhe do Erro"
        }
    )

    df_reordenada = df_renomeada[[
    "Tipo de Erro",
    "Tipo de Registro",
    "Número da Linha",
    "CHAVE",
    "Código do Erro",
    "Detalhe do Erro",
    "Conteúdo do Campo",
    "Impeditivo?",
    "UF",
    "CHAVE",
    "CHAVE"
    ]]

    return df_reordenada

def regras_negocio(df_reordenada):
    posicoes = [i for i, coluna in enumerate(df_reordenada.columns) if coluna == "CHAVE"]
    posicao = posicoes[-1]

    df_reordenada.iloc[:, posicao] = (
        df_reordenada.iloc[:, posicao]
        .astype(str)
        .str[:8]
    )

    mascara = df_reordenada['Tipo de Registro'] == '1-Curso'

    posicoes = [
        i
        for i, coluna in enumerate(df_reordenada.columns)
        if coluna == "CHAVE"
    ]

    ultimas_chaves = posicoes[-2:]

    df_reordenada.iloc[
        mascara.to_numpy(),
        ultimas_chaves
    ] = ""

    return df_reordenada

def exportando_excel(df_reordenada):
    caminho_saida = r"C:\Users\manoel.campos\OneDrive - SFIEMT\Área de Trabalho\AutomatizacaoDATACG\transformacao_excel\Critica_SGE.xlsx"
    df_reordenada.to_excel(caminho_saida, index=False,engine="xlsxwriter")
    print(f"Arquivo ajustado para envio: {caminho_saida}")
    return caminho_saida
