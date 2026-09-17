import os

pasta = os.path.join(os.path.expanduser("~"),"Downloads")

def criticas_downloads():
    arquivos = os.listdir(pasta)
    lista_arquivos_critica = []

    for arquivo in arquivos:
        if arquivo.startswith("Críticas_") and arquivo.endswith(".csv"):
            lista_arquivos_critica.append(arquivo)
    return lista_arquivos_critica

def caminhos_completos(lista_arquivos_critica):
    lista_caminhos_completos = []

    for arquivo_critica in lista_arquivos_critica:
        caminho = os.path.join(pasta, arquivo_critica)
        lista_caminhos_completos.append(caminho)
    return lista_caminhos_completos

def arquivo_recente(lista_caminho):
    if not lista_caminho:
        raise FileNotFoundError("Nenhum CSV de críticas foi encontrado em Downloads.")
    data_modificacoes = []

    for caminho in lista_caminho:
        data_modificacao = os.path.getmtime(caminho)
        data_modificacoes.append(data_modificacao)

    valor = max(data_modificacoes)
    posicao = data_modificacoes.index(valor)
    caminho_real = lista_caminho[posicao]

    print(f'Arquivo que vai para ajuste: {caminho_real}')
    return caminho_real

def buscar_ultima_critica():
    lista_criticas = criticas_downloads()
    lista_caminhos = caminhos_completos(lista_criticas)
    ultimo_arquivo = arquivo_recente(lista_caminhos)
    return ultimo_arquivo, True