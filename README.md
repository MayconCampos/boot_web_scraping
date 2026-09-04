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

## Credenciais

Nunca armazene logins ou senhas no Git. O arquivo `.gitignore` ignora `.env`, `credentials.json`, `secrets.json` e `config.local.py` para que arquivos locais de credenciais não sejam versionados.

Crie um arquivo `.env` na raiz do projeto com as variáveis abaixo:

```env
DATACG_LOGIN=seu_login_datacg
DATACG_PASSWORD=sua_senha_datacg
SHIFT_LOGIN=seu_login_shift
SHIFT_PASSWORD=sua_senha_shift
```

O arquivo `.env` local já foi configurado neste computador. Antes de enviar este projeto a um repositório remoto, revogue ou troque as senhas que já tenham sido expostas no histórico do Git.

## Execução

Com o ambiente virtual ativado:

```powershell
python main.py
```

O fluxo executa as etapas abaixo:

1. Baixa o CSV de críticas do DATACG.
2. Cria `transformacao_excel\Critica_SGE.xlsx` usando `XlsxWriter`.
3. Envia a planilha ao Shift.

## Gerar executável

Instale o empacotador no ambiente virtual e gere o executável:

```powershell
python -m pip install pyinstaller
pyinstaller --onefile --name AutomacaoDATACG main.py
```

O executável será criado em `dist\AutomacaoDATACG.exe`.
