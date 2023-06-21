import os
import shutil
from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from pytz import timezone

horario = '-1'
hora_inicio = "09:00"

while True:
    horario_atual = datetime.now()
    horario_tz = timezone('America/Sao_Paulo')
    horario_fuso = horario_atual.astimezone(horario_tz)
    horario = str(horario_fuso.strftime('%H:%M'))
    if horario == hora_inicio:
        # Variaveis
        dia_anterior = datetime.now() - timedelta(1)
        data = dia_anterior.strftime('%Y_%m_%d')
        data_bot = dia_anterior.strftime('%d/%m/%Y')
        horario = data

        # Copiar e renomear Catalogo antigo @jonas alterar diretorio
        os.rename("CatalogoEstaçõesAutomáticas.csv", "Backup_Catalogo_Auto_{}.csv".format(data))
        catalogo_antigo = r"C:/BotsPython/Inmet\\"
        backup_catalogo = r"C:/BotsPython/Inmet/backup_catalogo_auto\\"
        nome_catalogo = 'Backup_Catalogo_Auto_{}.csv'.format(data)

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
        driver = webdriver.Chrome('./chromedriver.exe')
        driver.get("https://portal.inmet.gov.br/paginas/catalogoaut")
        # driver.maximize_window()
        time.sleep(1)
        driver.find_element(by=By.XPATH, value=f"//*[@id='downloadcatalogo']").click()
        time.sleep(2)
        driver.close()

        # Mover arquivo para diretorio correto @jonas alterar diretorio
        caminho_catalogo = r"C:/Users/est985/Downloads\\CatalogoEstaçõesAutomáticas.csv"
        destino_catalogo = r"C:/BotsPython/Inmet/CatalogoEstaçõesAutomáticas.csv"
        shutil.move(caminho_catalogo, destino_catalogo)

        # Ler CSV
        df = pd.read_csv("CatalogoEstaçõesAutomáticas.csv", sep=';')
        for i, item in df.iterrows():
            try:
                estacao = item['CD_ESTACAO']

                # Abrir navegador
                driver = webdriver.Chrome('./chromedriver.exe')
                driver.get("https://tempo.inmet.gov.br/TabelaEstacoes/A001")

                # Abrir aba
                time.sleep(2)
                driver.find_element(by=By.CSS_SELECTOR,
                                    value=f"#root > div.ui.top.attached.header-container.menu > div.left.menu > i").click()

                # Escolher Automaticas
                time.sleep(2)
                driver.find_element(by=By.XPATH, value=f"//*[@id='root']/div[2]/div[1]/div[2]/div[1]/button[2]").click()
                time.sleep(1)
                driver.find_element(by=By.XPATH, value=f"//*[@id='root']/div[2]/div[1]/div[2]/div[1]/button[1]").click()

                # Escolher a estação
                time.sleep(2)
                escolher_estacao = driver.find_element(by=By.XPATH,
                                                       value=f"//*[@id='root']/div[2]/div[1]/div[2]/div[3]/input")
                escolher_estacao.click()
                escolher_estacao.send_keys('{}'.format(estacao))
                escolher_estacao.send_keys("\ue007")
                time.sleep(2)

                # Escolher as datas
                time.sleep(2)
                data_inicial = driver.find_element(by=By.XPATH,
                                                   value=f"//*[@id='root']/div[2]/div[1]/div[2]/div[4]/input")
                data_inicial.clear()
                data_inicial.send_keys('{}'.format(data_bot))
                data_inicial.send_keys("\ue007")
                data_final = driver.find_element(by=By.XPATH,
                                                 value=f"//*[@id='root']/div[2]/div[1]/div[2]/div[5]/input")
                data_final.clear()
                data_final.send_keys('{}'.format(data_bot))
                data_final.send_keys("\ue007")
                time.sleep(2)

                # Gerar tabela
                driver.find_element(by=By.XPATH, value=f"//*[@id='root']/div[2]/div[1]/div[2]/button").click()
                time.sleep(3)

                # Baixar CSV
                driver.find_element(by=By.XPATH, value=f"//*[@id='root']/div[2]/div[2]/div/div/div/span/a").click()
                time.sleep(2)
                driver.close()

                # Alterar arquivo
                caminho_estacao = r"C:/Users/est985/Downloads/generatedBy_react-csv.csv"
                destino_estacao = r"C:/BotsPython/Inmet//"
                shutil.move(caminho_estacao, destino_estacao)

                # Copiar e renomear Catalogo antigo
                os.rename("generatedBy_react-csv.csv", "{} {}.csv".format(estacao, data))


            except:
                pass

        time.sleep(20)

