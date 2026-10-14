import pyodbc
import pandas as pd
from config import _obter_variavel_obrigatoria

def obter_login():
    return _obter_variavel_obrigatoria("LOGIN_DB")

def obter_senha():
    return _obter_variavel_obrigatoria("PASSWORD_DB")

def connection_in_base():
    
    login_db = obter_login()
    password_db = obter_senha()
    
    connection = pyodbc.connect(
        "Driver={ODBC Driver 18 for SQL Server};"
        "Server=10.52.28.105;"
        f"UID={login_db};"
        f"PWD={password_db};"
        "TrustServerCertificate=yes"
    )
    
    cursor = connection.cursor()

    return cursor, connection

def consultation_in_base(cursor):
    cursor.execute(
        """
            SELECT 
                CodUnidadeOBA AS UNIDADE_ATENDIMENTO,
                CodEmpresa,
                FKCentroCusto
            FROM BIC_DW.Core.DimFilial
            WHERE CodEmpresa = '03MT'
            AND CodCentroIsValid = 'S'
            AND CodUnidadeOBA IS NOT NULL;
        """
    )
    
    values = cursor.fetchall()
    description = cursor.description
    
    return values, description

def analysis_base(values,description):
    colunas = [coluna[0] for coluna in description]
    
    df_analysis = pd.DataFrame.from_records(values, columns=colunas)
    
    df_analysis = df_analysis.rename(columns={
        'UNIDADE_ATENDIMENTO' : 'COD_UNIDADE_ATENDIMENTO',
        'FKCentroCusto' : 'FK_CENTRO_CUSTO'
    })
    
    df_analysis = df_analysis[['COD_UNIDADE_ATENDIMENTO','FK_CENTRO_CUSTO']]

    return df_analysis