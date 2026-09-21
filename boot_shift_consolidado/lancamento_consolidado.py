from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import os
from config import SHIFT_LOGIN, SHIFT_PASSWORD

def abrir_navegador():
    """Resumo: Abre o navegador Edge na página de login do Shift.

    Parâmetros: Nenhum.

    Retorno: Tupla com o navegador Selenium e sua espera explícita.
    """
    driver = webdriver.Edge()
    driver.maximize_window()
    driver.get("https://shift.sfiemt.ind.br:8043/login")
    wait = WebDriverWait(driver, 20)
    return driver, wait

def login(wait):
    """Resumo: Autentica o usuário no sistema Shift.

    Parâmetros: wait (WebDriverWait), espera explícita do Selenium.

    Retorno: Nenhum.
    """

    login_email = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//div[@class="login"]//input[@placeholder="Usuário"]')
            )
    )
    login_email.send_keys(SHIFT_LOGIN)


    login_password = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//div[@class="login"]//input[@placeholder="Senha"]')
            )
    )
    login_password.send_keys(SHIFT_PASSWORD)


    login_button = wait.until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, "p-button-label")
        )
    )

    login_button.click()

def aba_apuracao(driver,wait):
    """Resumo: Navega pelo menu do Shift até a área de apurações.

    Parâmetros: driver (WebDriver), navegador ativo; wait (WebDriverWait), espera explícita.

    Retorno: Nenhum.
    """

    menu = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "/html/body/app-root/app-main/div/div[1]")
        )
    )

    driver.execute_script(
        "arguments[0].scrollTop += 10000;",
        menu
    )


    drop_dall_gestao_estrategia = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//div[@class="menu-scroll-content"]//ul//li//span[normalize-space()="Gestão Estratégica"]')
            )
    )

    drop_dall_gestao_estrategia.click()


    drop_dall_gestao_relarotio_gerencial = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//span[normalize-space()="Relatório Gerencial"]')
            )
    )

    drop_dall_gestao_relarotio_gerencial.click()


    selecionando_apuracao = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//span[normalize-space()="Apurações"]')
            )
    )

    selecionando_apuracao.click()

def importando_critica(wait,mes_importacao, ano_importacao):
    """Resumo: Seleciona o ciclo e o período da crítica a importar.

    Parâmetros: wait (WebDriverWait), espera; mes_importacao (str), mês; ano_importacao (int), ano.

    Retorno: Nenhum.
    """



    selecionando_apuracao = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//p-checkbox/div/div[2]/span')
            )
    )

    selecionando_apuracao.click()


    drop_dall_campo_ciclo = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="pr_id_11_label"]')
            )
    )

    drop_dall_campo_ciclo.click()


    ano =  ano_importacao
    drop_dall_ciclo = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, f'//span[normalize-space()="REFORMULACAO-{ano}"]')
            )
    )

    drop_dall_ciclo.click()


    mes = mes_importacao
    mes = mes.upper()
    lupa_mes_desejado = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, f'//tr[.//td[normalize-space()="{mes}"]]//button[@ptooltip="Detalhar"]')
        )
    )

    lupa_mes_desejado.click()

def anexando_critica(driver, wait):
    """Resumo: Anexa a planilha de críticas e confirma seu envio ao Shift.

    Parâmetros: driver (WebDriver), navegador ativo; wait (WebDriverWait), espera explícita.

    Retorno: Nenhum.
    """

    botao_selecionar_arquivo = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//button[@icon="pi pi-chevron-down"]')
        )
    )

    botao_selecionar_arquivo.click()

    botao_selecionar_arquivo = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//span[contains(@class, "p-menuitem-text") and normalize-space()="Produção EPS"]')
        )
    )

    botao_selecionar_arquivo.click()




    pasta_atual = os.path.dirname(__file__)
    raiz_projeto = os.path.dirname(pasta_atual)

    caminho_arquivo = os.path.join(
        raiz_projeto,
        "Ajuste_base_consolidado",
        "Resultado_oficial_consolidado.xlsx"
    )

    input_arquivo = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                '//input[@formcontrolname="arquivo" and @type="file"]'
            )
        )
    )

    input_arquivo.send_keys(caminho_arquivo)


    botao_salvar = WebDriverWait(
        driver, 20, ignored_exceptions=(StaleElementReferenceException,)
    ).until(
        EC.element_to_be_clickable(
            (By.XPATH,'//button[.//span[normalize-space()="Salvar"]]')
        )
    )

    botao_salvar.click()
 
    wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//p-toastitem[contains(., 'Sucesso!')"
            )
        )
    )

    print("Arquivo publicado com sucesso.")
