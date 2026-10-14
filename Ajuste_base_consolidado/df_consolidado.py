from pathlib import Path
import pandas as pd


def transformar_consolidado(caminho_csv, df_analysis):
    """Resumo: Transforma os dados do Resultado Oficial no layout de envio do consolidado.

    Parâmetros: caminho_csv (str ou Path), CSV desta execução; df_analysis (DataFrame), relação de unidades e centros de custo.

    Retorno: DataFrame com as 50 colunas ordenadas, identificadores preservados e datas convertidas.
    """
    df_analysis = df_analysis.copy()
    df_analysis['COD_UNIDADE_ATENDIMENTO'] = df_analysis['COD_UNIDADE_ATENDIMENTO'].astype('string').str.strip()
    df_eps = pd.read_csv(
        caminho_csv,
        sep=",",
        encoding="utf-8",
        dtype="string",
        keep_default_na=False,
        na_values=[""],
        usecols=[
            "TIPO_ACAO",
            "CH_CURSO_PRESENCIAL",
            "QT_HORAS_PRATICA_PROFISSIONAL",
            "MODALIDADE",
            "TIPO_FINANCIAMENTO",
            "ESCOLA_ORIGEM",
            "UNIDADE_ATENDIMENTO",
            "AH_FASE_ESCOLAR_ANO",
            "AH_FASE_ESTAGIO_ANO",
            "AH_PRATICA_ANO",
            "HORA_ALUNO",
            "HORA_ALUNO_EAD",
            "ARTICULA_SESI_SENAI",
            "CH_CURSO_EAD",
            "CH_CURSO_FASE_ESTAGIO",
            "CNPJ_EMPRESA_ATENDIDA",
            "CD_ALUNO",
            "AREA_ATUACAO",
            "CATEGORIA",
            "RACA_COR_ALUNO",
            "CD_CURSO",
            "LINHA_ACAO",
            "CD_MATRICULA",
            "MUNICIPIO_ACAO",
            "CPF_ALUNO",
            "DT_ENTRADA",
            "DT_INICIO_CONTRATO",
            "DT_INICIO_OFERTA_CURSO",
            "DT_NASC_ALUNO",
            "DT_SAIDA",
            "DT_SAIDA_PREVISTA",
            "DT_FIM_CONTRATO",
            "DT_TERMINO_OFERTA_CURSO",
            "NIV_ESCOLARIDADE_ALUNO",
            "ESTADO_CIVIL_ALUNO",
            "FPAS",
            "INDUSTRIA",
            "FL_LOJA_NACIONAL",
            "NACIONALIDADE_ALUNO",
            "NATURALIDADE_ALUNO",
            "NECESSID_ESPECIAL_ALUNO",
            "NOME_ALUNO",
            "SIT_OCUPACIONAL_ALUNO",
            "SEXO_ALUNO",
            "SITUACAO_MATRICULA",
            "TIPO_AMBIENTE",
            "TIPO_ENTRADA_ALUNO",
            "TIPO_MATRICULA",
            "RESP_FIN_CNPJ",
        ],
    )

    # Ajustando os texto
    colunas = df_eps.columns

    for coluna in colunas:
        df_eps[coluna] = df_eps[coluna].str.strip().str.upper()


    # Renomeando as colunas que iram ter os códigos extraídos
    df_eps = df_eps.rename(
        columns={
            "TIPO_ACAO": "COD_TIPO_ACAO",
            "MODALIDADE": "COD_MODALIDADE",
            "TIPO_FINANCIAMENTO": "COD_TIPO_FINANCIAMENTO",
            "ESCOLA_ORIGEM": "COD_TIPO_ESCOLA_ORIGEM",
            "UNIDADE_ATENDIMENTO": "COD_UNIDADE_ATENDIMENTO",
            "AREA_ATUACAO": "COD_AREA_ATUACAO",
            "CATEGORIA": "COD_CATEGORIA",
            "RACA_COR_ALUNO": "COD_RACA_COR_ALUNO",
            "LINHA_ACAO": "COD_LINHA_ACAO",
            "NIV_ESCOLARIDADE_ALUNO": "COD_NIV_ESCOLARIDADE_ALUNO",
            "ESTADO_CIVIL_ALUNO": "COD_ESTADO_CIVIL_ALUNO",
            "NECESSID_ESPECIAL_ALUNO": "COD_NECESSID_ESPECIAL_ALUNO",
            "SIT_OCUPACIONAL_ALUNO": "COD_SIT_OCUPACIONAL_ALUNO",
            "SITUACAO_MATRICULA": "COD_SITUACAO_MATRICULA",
            "TIPO_AMBIENTE": "COD_TIPO_AMBIENTE",
            "TIPO_ENTRADA_ALUNO": "COD_TIPO_ENTRADA_ALUNO",
        }
    )


    # Extração dos códigos
    colunas = [
        "COD_TIPO_ACAO",
        "COD_MODALIDADE",
        "COD_TIPO_FINANCIAMENTO",
        "COD_TIPO_ESCOLA_ORIGEM",
        "COD_UNIDADE_ATENDIMENTO",
        "COD_AREA_ATUACAO",
        "COD_CATEGORIA",
        "COD_RACA_COR_ALUNO",
        "COD_LINHA_ACAO",
        "COD_NIV_ESCOLARIDADE_ALUNO",
        "COD_ESTADO_CIVIL_ALUNO",
        "COD_NECESSID_ESPECIAL_ALUNO",
        "COD_SIT_OCUPACIONAL_ALUNO",
        "COD_SITUACAO_MATRICULA",
        "COD_TIPO_AMBIENTE",
        "COD_TIPO_ENTRADA_ALUNO",
    ]

    for coluna in colunas:
        df_eps[coluna] = df_eps[coluna].str.split(" ", n=1).str[0]


    # Definindo os códigos para coluna
    map_cod = {
        "NOVA": 1,
        "TRANSFERENCIA": 2,
        "RESIDUAL": 5,
    }

    df_eps["COD_TIPO_MATRICULA"] = df_eps["TIPO_MATRICULA"].map(map_cod)
    df_eps["COD_TIPO_MATRICULA"] = df_eps["COD_TIPO_MATRICULA"].fillna(0)
    df_eps["COD_TIPO_MATRICULA"] = df_eps["COD_TIPO_MATRICULA"].astype("Int64")


    # Join com db.ipynb para trazer os CentroCusto
    df_eps = df_eps.merge(df_analysis, how="left", on="COD_UNIDADE_ATENDIMENTO", validate="many_to_one")


    # Pegando o código do municipio
    df_eps["MUNICIPIO_ACAO"] = df_eps["MUNICIPIO_ACAO"].str.extract(r"\((\d+)\)")
    df_eps = df_eps.rename(columns={"MUNICIPIO_ACAO": "COD_MUNICIPIO"})


    # Pegando o código de Naturalidade
    df_eps["NATURALIDADE_ALUNO"] = df_eps["NATURALIDADE_ALUNO"].str.extract(r"\((\d+)\)")
    df_eps = df_eps.rename(columns={"NATURALIDADE_ALUNO": "COD_NATURALIDADE_ALUNO"})


    # Corrigindo datas:
    colunas_data = [
        "DT_ENTRADA",
        "DT_INICIO_CONTRATO",
        "DT_INICIO_OFERTA_CURSO",
        "DT_NASC_ALUNO",
        "DT_SAIDA",
        "DT_SAIDA_PREVISTA",
        "DT_FIM_CONTRATO",
        "DT_TERMINO_OFERTA_CURSO",
    ]

    for coluna in colunas_data:

        # Guarda os textos antes da conversão.
        texto = df_eps[coluna]

        # Primeira tentativa: ano-mês-dia.
        # Exemplo: 2023-06-05.
        datas_iso = pd.to_datetime(
            texto,
            format="%Y-%m-%d",
            errors="coerce",
        )

        # Segunda tentativa: dia/mês/ano.
        # Exemplo: 05/06/2023.
        datas_brasileiras = pd.to_datetime(
            texto,
            format="%d/%m/%Y",
            errors="coerce",
        )
        # Onde a primeira tentativa não encontrou uma data,
        # usa o resultado da segunda tentativa.
        datas = datas_iso.fillna(datas_brasileiras)

        # Um texto preenchido não deve desaparecer silenciosamente.
        # Se nenhum formato conseguiu interpretá-lo, precisamos investigar.
        invalidas = texto.notna() & datas.isna()

        if invalidas.any():
            raise ValueError("Existem datas inválidas na coluna: " + coluna)

        # Salva as datas reais no DataFrame.
        df_eps[coluna] = datas.dt.date


    # Ajustando Horas:
    colunas_horas = [
        "HORA_ALUNO",
        "HORA_ALUNO_EAD",
    ]

    for coluna in colunas_horas:

        # Na leitura, preservamos o texto "null".
        # Nessas duas colunas, ele representa uma ausência.
        df_eps[coluna] = df_eps[coluna].replace("NULL", pd.NA)

        # Converte para número.
        # Um texto inesperado gera erro para você investigar.
        df_eps[coluna] = pd.to_numeric(df_eps[coluna], errors="raise")

        # Inteiro que aceita valores ausentes.
        df_eps[coluna] = df_eps[coluna].astype("Int64")


    # Reordenando para ordem de envio
    df_eps = df_eps[
        [
            "COD_TIPO_ACAO",
            "CH_CURSO_PRESENCIAL",
            "QT_HORAS_PRATICA_PROFISSIONAL",
            "COD_MODALIDADE",
            "COD_TIPO_FINANCIAMENTO",
            "COD_TIPO_ESCOLA_ORIGEM",
            "FK_CENTRO_CUSTO",
            "AH_FASE_ESCOLAR_ANO",
            "AH_FASE_ESTAGIO_ANO",
            "AH_PRATICA_ANO",
            "HORA_ALUNO",
            "HORA_ALUNO_EAD",
            "ARTICULA_SESI_SENAI",
            "CH_CURSO_EAD",
            "CH_CURSO_FASE_ESTAGIO",
            "CNPJ_EMPRESA_ATENDIDA",
            "CD_ALUNO",
            "COD_AREA_ATUACAO",
            "COD_CATEGORIA",
            "COD_RACA_COR_ALUNO",
            "CD_CURSO",
            "COD_LINHA_ACAO",
            "CD_MATRICULA",
            "COD_MUNICIPIO",
            "COD_UNIDADE_ATENDIMENTO",
            "CPF_ALUNO",
            "DT_ENTRADA",
            "DT_INICIO_CONTRATO",
            "DT_INICIO_OFERTA_CURSO",
            "DT_NASC_ALUNO",
            "DT_SAIDA",
            "DT_SAIDA_PREVISTA",
            "DT_FIM_CONTRATO",
            "DT_TERMINO_OFERTA_CURSO",
            "COD_NIV_ESCOLARIDADE_ALUNO",
            "COD_ESTADO_CIVIL_ALUNO",
            "FPAS",
            "INDUSTRIA",
            "FL_LOJA_NACIONAL",
            "NACIONALIDADE_ALUNO",
            "COD_NATURALIDADE_ALUNO",
            "COD_NECESSID_ESPECIAL_ALUNO",
            "NOME_ALUNO",
            "COD_SIT_OCUPACIONAL_ALUNO",
            "SEXO_ALUNO",
            "COD_SITUACAO_MATRICULA",
            "COD_TIPO_AMBIENTE",
            "COD_TIPO_ENTRADA_ALUNO",
            "COD_TIPO_MATRICULA",
            "RESP_FIN_CNPJ",
        ]
    ]

    return df_eps


def disparar_ajuste_consolidado(caminho_csv, caminho_saida=None, centros=None):
    """Resumo: Consulta os centros de custo, transforma o consolidado e salva a planilha.

    Parâmetros: caminho_csv (str ou Path), CSV baixado; caminho_saida (str ou Path, opcional), destino do Excel; centros (DataFrame, opcional), relação já consultada para testes locais.

    Retorno: Path absoluto do Excel gerado. Erros de leitura, transformação ou exportação interrompem o fluxo.
    """
    caminho_csv = Path(caminho_csv).resolve(strict=True)
    if centros is None:
        from .centro_custo import connection_in_base, consultation_in_base, analysis_base
        cursor, connection = connection_in_base()
        try:
            valores, descricao = consultation_in_base(cursor)
            centros = analysis_base(valores, descricao)
        finally:
            cursor.close()
            connection.close()
    resultado = transformar_consolidado(caminho_csv, centros)
    if caminho_saida is None:
        caminho_saida = caminho_csv.parent / (caminho_csv.stem + '_tratado.xlsx')
    caminho_saida = Path(caminho_saida).resolve()
    with pd.ExcelWriter(caminho_saida, engine='xlsxwriter', date_format='dd/mm/yyyy', datetime_format='dd/mm/yyyy') as writer:
        resultado.to_excel(writer, index=False)
    return caminho_saida
