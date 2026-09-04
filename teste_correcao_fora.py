import pandas as pd


# ============================================================
# 1. LER O ARQUIVO EXCEL
# ============================================================

df_critica_sge_pura = pd.read_csv(
    r'C:\Users\manoel.campos\Downloads\Críticas_1811.csv',
    dtype=str
)


# ============================================================
# 2. RENOMEAR AS COLUNAS
# ============================================================

df_renomeada = df_critica_sge_pura.rename(
    columns={
        "TIPO_ERRO": "Tipo de Erro",
        "TIPO_REGISTRO": "Tipo de Registro",
        "NR_LINHA": "Número da Linha",
        "codigo_erro_individual": "Código do Erro",
        "CONTEUDO_DO_CAMPO": "Conteúdo do Campo",
        "IMPEDITIVO?": "Impeditivo?",
        "DESC_ERRO": "Detalhe do Erro"
    }
)


# ============================================================
# 3. REORDENAR AS COLUNAS
# ============================================================

df_reordenada = df_renomeada[
    [
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
    ]
].copy()


# ============================================================
# 4. LOCALIZAR AS COLUNAS CHAVE
# ============================================================

posicoes_chave = [
    i
    for i, coluna in enumerate(df_reordenada.columns)
    if coluna == "CHAVE"
]

print("Posições das CHAVE:", posicoes_chave)


# ============================================================
# 5. PEGAR A ÚLTIMA CHAVE E DEIXAR SOMENTE OS 8 PRIMEIROS
#    CARACTERES
# ============================================================

ultima_chave = posicoes_chave[-1]

df_reordenada.iloc[:, ultima_chave] = (
    df_reordenada.iloc[:, ultima_chave]
    .astype(str)
    .str[:8]
)


# ============================================================
# 6. IDENTIFICAR AS LINHAS QUE SÃO 1-Curso
# ============================================================

mascara = df_reordenada["Tipo de Registro"] == "1-Curso"


# ============================================================
# 7. PEGAR AS DUAS ÚLTIMAS CHAVE
# ============================================================

ultimas_chaves = posicoes_chave[-2:]


# ============================================================
# 8. NAS LINHAS 1-Curso, LIMPAR AS DUAS ÚLTIMAS CHAVE
# ============================================================

df_reordenada.iloc[
    mascara.to_numpy(),
    ultimas_chaves
] = ""


# ============================================================
# 9. EXPORTAR O ARQUIVO
# ============================================================

df_reordenada.to_excel(
    r"C:\Users\manoel.campos\OneDrive - SFIEMT\Área de Trabalho\AutomatizacaoDATACG\transformacao_excel\NOVO.xlsx",
    index=False,engine="xlsxwriter"
)
print(df_reordenada)
print("Arquivo transformado com sucesso!")