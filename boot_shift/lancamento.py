from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time

from config import SHIFT_LOGIN, SHIFT_PASSWORD

def abrir_navegador():
    driver = webdriver.Edge()
    driver.maximize_window()
    driver.get("https://shift.sfiemt.ind.br:8043/login")
    wait = WebDriverWait(driver, 20)
    return driver, wait

def login(wait):
    #Campo email
    login_email = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//div[@class="login"]//input[@placeholder="Usuário"]')
            )
    )
    login_email.send_keys(SHIFT_LOGIN)

    #Campo senha
    login_password = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//div[@class="login"]//input[@placeholder="Senha"]')
            )
    )
    login_password.send_keys(SHIFT_PASSWORD)

    #Logando no sistema
    login_button = wait.until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, "p-button-label")
        )
    )

    login_button.click()

def aba_apuracao(driver,wait):
    #Scroll do menu lateral
    menu = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "/html/body/app-root/app-main/div/div[1]")
        )
    )

    driver.execute_script(
        "arguments[0].scrollTop += 10000;",
        menu
    )

    #Primeiro menu para clicar
    drop_dall_gestao_estrategia = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//div[@class="menu-scroll-content"]//ul//li//span[normalize-space()="Gestão Estratégica"]')
            )
    )

    drop_dall_gestao_estrategia.click()

    #Segundo menu para clicar
    drop_dall_gestao_relarotio_gerencial = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//span[normalize-space()="Relatório Gerencial"]')
            )
    )

    drop_dall_gestao_relarotio_gerencial.click()

    #Segundo menu para clicar
    selecionando_apuracao = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//span[normalize-space()="Apurações"]')
            )
    )

    selecionando_apuracao.click()

def importando_critica(wait):
    #Subindo o arquivo critica

    #Desativando o botão de "Apuração Ativa?"
    selecionando_apuracao = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//p-checkbox/div/div[2]/span')
            )
    )

    selecionando_apuracao.click()

    #Selecionando o dropdown de ciclo
    drop_dall_campo_ciclo = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="pr_id_11_label"]')
            )
    )

    drop_dall_campo_ciclo.click()

    #Selecionando o ciclo
    drop_dall_ciclo = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//span[normalize-space()="REFORMULACAO-2026"]')
            )
    )

    drop_dall_ciclo.click()

    #Selecionando o mês de Agosto
    # //*//button[@ptooltip="Detalhar"] -> Agosto
    lupa_mes_desejado = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//tr[.//td[normalize-space()="SETEMBRO"]]//button[@ptooltip="Detalhar"]')
        )
    )

    lupa_mes_desejado.click()

def anexando_critica(driver, wait):
    #Janela para subir arquivo
    botao_selecionar_arquivo = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//p-toolbar[@class="p-element"]//button[@title="Upload Dados"]')
        )
    )

    botao_selecionar_arquivo.click()

    #Selcionando Origem
    botao_selecionar_arquivo = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//p-dropdown[@placeholder="Selecione a origem"]//span[normalize-space()="Selecione a origem"]')
        )
    )

    botao_selecionar_arquivo.click()

    #Selecionando origem 
    botao_selecionar_arquivo = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//div[@class="p-dropdown-items-wrapper"]//li[@aria-label="SI - CRÍTICAS PRODUÇÃO EPS"]')
        )
    )

    botao_selecionar_arquivo.click()

    # Envia o arquivo diretamente ao input. Não clicar no dropzone evita abrir
    # a janela nativa do Windows, que o Selenium não consegue fechar.
    caminho_arquivo = r"C:\Users\manoel.campos\OneDrive - SFIEMT\Área de Trabalho\AutomatizacaoDATACG\transformacao_excel\Critica_SGE.xlsx"

    input_arquivo = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                '//*[@class="upload-dropzone"]//input[@type="file"]'
            )
        )
    )

    input_arquivo.send_keys(caminho_arquivo)

    #Salvando arquivo
    botao_salvar = WebDriverWait(
        driver, 20, ignored_exceptions=(StaleElementReferenceException,)
    ).until(
        EC.element_to_be_clickable(
            (By.XPATH,'//button[.//span[normalize-space()="Salvar"]]')
        )
    )

    botao_salvar.click()
    print('Fim do processo arquivo publicado')
    time.sleep(30)
