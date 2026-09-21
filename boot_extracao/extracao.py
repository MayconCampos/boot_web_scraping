from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import time
import os
from config import DATACG_LOGIN, DATACG_PASSWORD

# Define a pasta padrão em que o navegador salva os relatórios extraídos.
PASTA_DOWNLOAD =  os.path.join(os.path.expanduser("~"),"Downloads")
PASTA_DOWNLOAD = Path(PASTA_DOWNLOAD)

def abrir_navegador():
    """Resumo: Abre o navegador Chrome na página de login do DataCG.

    Parâmetros: Nenhum.

    Retorno: Tupla com o navegador Selenium e sua espera explícita.
    """
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://datacg.sistemaindustria.com.br/login")
    wait = WebDriverWait(driver, 20)
    return driver,wait

def login_sistema(wait):
    """Resumo: Autentica o usuário no sistema DataCG.

    Parâmetros: wait (WebDriverWait), espera explícita do Selenium.

    Retorno: True após o acionamento do login.
    """
    login_email = wait.until(
        EC.element_to_be_clickable((By.ID, "mat-input-0"))
    )
    login_email.send_keys(DATACG_LOGIN)

    login_password = wait.until(
        EC.element_to_be_clickable((By.ID, "mat-input-1"))
    )
    login_password.send_keys(DATACG_PASSWORD)

    login_button = wait.until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, "mat-button-wrapper")
        )
    )

    login_button.click()
    return True


def perfis_acesso(wait):
    """Resumo: Seleciona o perfil de acesso de produção no DataCG.

    Parâmetros: wait (WebDriverWait), espera explícita do Selenium.

    Retorno: True após confirmar o perfil selecionado.
    """
    access_profile = wait.until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, "full-width-input")
        )
    )
    access_profile.click()



    system_profile = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//mat-option[.//span[normalize-space()='DL- Produção EP']]")
        )
    )
    system_profile.click()


    profile_confirm = wait.until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, 'submit-btn')
        )
    )
    profile_confirm.click()
    return True

def gerando_relatorio(wait,mes_importacao, ano_importacao):
    """Resumo: Configura e confirma a geração do relatório de críticas.

    Parâmetros: wait (WebDriverWait), espera do Selenium; mes_importacao (str), mês; ano_importacao (int), ano.

    Retorno: True após confirmar os filtros do relatório.
    """

    menu_report = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH,"//button[@title='Relatórios']")
            )
    )
    menu_report.click()


    more = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@routerlink='cadastrar']")
            )
    )
    more.click()


    time.sleep(0.5)


    cargo_type = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//mat-select[@placeholder='Tipo de carga']//div[contains(@class,'mat-select-trigger')]")
            )
    )
    cargo_type.click()


    campo_critica = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//mat-option[.//span[normalize-space()='Críticas']]")
        )
    )
    campo_critica.click()


    month_field = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//mat-select[@placeholder='Mês']")
            )
    )
    month_field.click()


    mes = mes_importacao
    month = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//mat-option[.//span[normalize-space()='{mes}']]")
        )
    )

    month.click()


    year_field = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//mat-select[@placeholder='Ano']")
        )
    )

    year_field.click()


    ano = ano_importacao
    year = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//mat-option[.//span[normalize-space()='{ano}']]")
        )
    )

    year.click()


    confirm_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//biview-export-dialog//button[contains(@class, 'submit-btn')]")
        )
    )

    confirm_button.click()

    return True

def exportando_computador(driver, wait, timeout=200):
    """Resumo: Inicia a exportação do relatório para o computador.

    Parâmetros: driver (WebDriver), navegador ativo; wait (WebDriverWait), espera; timeout (int), limite em segundos.

    Retorno: Conjunto com os nomes de arquivos existentes antes do download.
    """


    wait.until(
        EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, ".cdk-overlay-backdrop")
        )
    )


    element_correto = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="main-container"]/biview-export-list/div/biview-table-list-content/div/table/tbody/tr[1]/td[6]/button')
        )
    )
    arquivos_antes = {arquivo.name for arquivo in PASTA_DOWNLOAD.iterdir()}

    element_correto.click()
    return arquivos_antes

def aguardar_novo_download(arquivos_antes, timeout=200):
    """Resumo: Aguarda a conclusão e estabilização do novo CSV de críticas.

    Parâmetros: arquivos_antes (set), arquivos existentes antes da exportação; timeout (int), limite em segundos.

    Retorno: Caminho do CSV novo concluído.
    """
    limite = time.monotonic() + timeout
    ultimo_tamanho = {}

    while time.monotonic() < limite:
        candidatos = [
            arquivo for arquivo in PASTA_DOWNLOAD.glob("Críticas_*.csv")
            if arquivo.name not in arquivos_antes
        ]

        for arquivo in candidatos:
            temporario = arquivo.with_name(f"{arquivo.name}.crdownload")
            if temporario.exists():
                continue

            tamanho_atual = arquivo.stat().st_size
            if tamanho_atual > 0 and ultimo_tamanho.get(arquivo) == tamanho_atual:
                return arquivo
            ultimo_tamanho[arquivo] = tamanho_atual

        time.sleep(2)

    raise TimeoutError(
        f"Nenhum novo CSV de críticas foi concluído em {timeout} segundos."
    )
