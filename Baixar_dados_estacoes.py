import pyautogui
from selenium import webdriver
import os
import time
import shutil
import pandas as pd
from datetime import date, datetime, timedelta

# Variaveis
contagem = 0
contagem_data = 0
dia_anterior = datetime.now() - timedelta(1)
data = dia_anterior.strftime('%Y_%m_%d')
data_bot = dia_anterior.strftime('%d/%m/%Y')

# Copiar e renomear Catalogo antigo
os.rename("CatalogoEstaçõesConvencionais.csv", "Backup_Catalogo_{}.csv".format(data))
catalogo_antigo = r"C:/Users/est985/Documents/Python/bot_chesf//"
backup_catalogo = r"C:/Users/est985/Documents/Python/bot_chesf/Catalogo_estacoes\\"
nome_catalogo = 'Backup_Catalogo_{}.csv'.format(data)

# Conferir arquivo
if os.path.exists(backup_catalogo + nome_catalogo):
    # Separar nome da extensao
    data_catalogo = os.path.splitext(nome_catalogo)
    only_name = data_catalogo[0]
    extensao = data_catalogo[1]
    # Alterar nome
    nova_base = only_name + '{}'.format(data) + extensao
    # Construir caminho
    novo_nome = os.path.join(backup_catalogo, nova_base)
    # Mover arquivo
    shutil.move(catalogo_antigo + nome_catalogo, novo_nome)
else:
    shutil.move(catalogo_antigo + nome_catalogo, backup_catalogo + nome_catalogo)

# Baixar Catalogo
pyautogui.press("Win")
time.sleep(3)
pyautogui.write("edge")
time.sleep(3)
pyautogui.press("Enter")
time.sleep(3)
pyautogui.write("https://portal.inmet.gov.br/paginas/catalogoman#")
time.sleep(4)
pyautogui.press("Enter")
time.sleep(4)
pyautogui.click(1568, 343)
time.sleep(4)
pyautogui.click(1556, 156)
time.sleep(4)
pyautogui.press("Enter")
time.sleep(4)
pyautogui.click(1897, 16)

# Mover arquivo para diretorio correto
caminho_catalogo = r"C:/Users/est985/Documents/Python/bot_chesf/Dados_estacoes/CatalogoEstaçõesConvencionais.csv"
destino_catalogo = r"C:/Users/est985/Documents/Python/bot_chesf/CatalogoEstaçõesConvencionais.csv"
shutil.move(caminho_catalogo, destino_catalogo)

# Abrir navegador
time.sleep(3)
pyautogui.press("Win")
time.sleep(2)
pyautogui.write("edge")
pyautogui.press("Enter")
time.sleep(3.5)
pyautogui.write("https://tempo.inmet.gov.br/TabelaEstacoes/A001")
pyautogui.press("Enter")

# Ler CSV
df = pd.read_csv("CatalogoEstaçõesConvencionais.csv", sep=';')
for i, item in df.iterrows():
    estacao = item['CD_ESTACAO']

    # Abrir aba
    time.sleep(4)
    pyautogui.click(30, 97)

    # Escolher Convencionais
    if contagem == 0:
        time.sleep(2)
        pyautogui.click(188, 279)
        contagem += 1

    # Escolher a estação
    time.sleep(2)
    pyautogui.click(223, 430)
    pyautogui.write("{}".format(estacao))
    pyautogui.press("enter")

    # Escolher as datas
    if contagem_data == 0:
        time.sleep(4)
        pyautogui.press("tab")
        pyautogui.typewrite('{}'.format(data_bot))
        time.sleep(2)
        pyautogui.press("enter")
        pyautogui.press("tab")
        time.sleep(1)
        pyautogui.typewrite('{}'.format(data_bot))
        time.sleep(2)
        pyautogui.press("enter")
        contagem_data += 1

    # Gerar tabela
    time.sleep(2)
    pyautogui.click(130, 637)

    # Baixar CSV
    time.sleep(2)
    pyautogui.click(947, 230)

    # Salvar nome do arquivo
    time.sleep(4)
    pyautogui.click(1556, 156)
    time.sleep(4)
    pyautogui.write("{} {}".format(estacao, data))
    time.sleep(2)
    pyautogui.press("Enter")
    time.sleep(4)
