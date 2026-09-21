# Automação DATACG

Automação em Python que baixa o relatório de críticas no DATACG, transforma o CSV em uma planilha Excel compatível e envia o arquivo ao Shift.

## Pré-requisitos

- Python 3.10 ou superior
- Google Chrome e Microsoft Edge instalados
- Acesso aos sistemas DATACG e Shift

## Instalação

No PowerShell, na raiz do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Execução

Com o ambiente virtual ativado:

```powershell
python main.py
```

O fluxo executa as etapas abaixo:

1. Baixa o CSV de críticas do DATACG.
2. Cria `Ajuste_base_critica\Critica_SGE.xlsx` usando `XlsxWriter`.
3. Envia a planilha ao Shift.

## Gerar executável

Instale o empacotador no ambiente virtual e gere o executável:

```powershell
python -m pip install pyinstaller
pyinstaller --onefile --name AutomacaoDATACG main.py
```

O executável será criado em `dist\AutomacaoDATACG.exe`.
