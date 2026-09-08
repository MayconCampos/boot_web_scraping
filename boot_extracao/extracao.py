from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import time
from config import DATACG_LOGIN, DATACG_PASSWORD
from conf_geral import data_referencia


PASTA_DOWNLOAD = Path(r"C:\Users\manoel.campos\Downloads")


def abrir_navegador():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://datacg.sistemaindustria.com.br/login")
    wait = WebDriverWait(driver, 20)
    return driver,wait 

def login_sistema(wait):
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

# Dropdown de perfis de acesso
def perfis_acesso(wait):
    access_profile = wait.until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, "full-width-input")
        )
    )
    access_profile.click()


    # Selecionando perfil
    system_profile = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//mat-option[.//span[normalize-space()='DL- Produção EP']]")
        )
    )
    system_profile.click()

    # Entrando no sistema
    profile_confirm = wait.until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, 'submit-btn')
        )
    )
    profile_confirm.click()
    return True

def gerando_relatorio(wait):
    # Menu do relatório
    menu_report = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH,"//button[@title='Relatórios']")
            )
    )
    menu_report.click()

    #clicando no +
    more = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@routerlink='cadastrar']")
            )
    )
    more.click()
    # O modal Angular precisa concluir a renderização antes de abrir o select.
    # Esta espera fazia parte do fluxo que funcionava anteriormente.
    time.sleep(0.5)

    #Selecionando o dropdown
    cargo_type = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//mat-select[@placeholder='Tipo de carga']//div[contains(@class,'mat-select-trigger')]")
            )
    )
    cargo_type.click()

    #Selecionando critica
    campo_critica = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//mat-option[.//span[normalize-space()='Críticas']]")
        )
    )
    campo_critica.click()

    #Selecionando campo mês
    month_field = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//mat-select[@placeholder='Mês']")
            )
    )
    month_field.click()

    #Selecionando mês
    mes, _ = data_referencia(False)
    month = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//mat-option[.//span[normalize-space()='{mes}']]")
        )
    )

    month.click()

    #Selecionando campo ano
    year_field = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//mat-select[@placeholder='Ano']")
        )
    )

    year_field.click()

    #Selecionando ano
    _  , ano = data_referencia()
    year = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//mat-option[.//span[normalize-space()='{ano}']]")
        )
    )

    year.click()

    #confirmando filtros
    confirm_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//biview-export-dialog//button[contains(@class, 'submit-btn')]")
        )       
    )

    confirm_button.click()

    return True

def exportando_computador(driver, wait, timeout=180):

     # Espera o overlay desaparecer
    wait.until(
        EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, ".cdk-overlay-backdrop")
        )
    )

    # Importando o arquivo para o computador
    element_correto = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="main-container"]/biview-export-list/div/biview-table-list-content/div/table/tbody/tr[1]/td[6]/button')
        )
    )
    arquivos_antes = {arquivo.name for arquivo in PASTA_DOWNLOAD.iterdir()}
    element_correto.click()
    return arquivos_antes

def aguardar_novo_download(arquivos_antes, timeout=180):
    """Retorna o CSV de crítica criado nesta execução após ele estabilizar."""
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

        time.sleep(1)

    raise TimeoutError(
        f"Nenhum novo CSV de críticas foi concluído em {timeout} segundos."
    )
