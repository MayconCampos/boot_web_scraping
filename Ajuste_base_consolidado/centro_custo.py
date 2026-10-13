import pyodbc
import pandas as pd
from config import LOGIN_DB, PASSWORD_DB

def connection_in_base():
    connection = pyodbc.connect(
        "Driver={ODBC Driver 18 for SQL Server};"
        "Server=10.52.28.105;"
        f"UID={LOGIN_DB};"
        f"PWD={PASSWORD_DB};"
        "TrustServerCertificate=yes"
    )
    
    cursor = connection.cursor()
    
    return cursor

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
