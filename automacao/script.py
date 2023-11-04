import os
import time
import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# configurações
url_plataforma = ("https://monitoramento-precos.netlify.app")
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")

# caminho para o chromedriver
# chromedriver_path = "../drivers/chromedriver.exe"

# criando o serviço
# service = Service(chromedriver_path)

# inicializa o driver do Selenium
driver = webdriver.Chrome(options=chrome_options)


# função para pegar o preço atual na página
def pegar_preco():
    preco = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#product-price"))
    ).text
    return float(preco.replace("R$", "").strip())


# função para enviar notificação para o Slack
def enviar_notificacao_slack(mensagem):
    slack_webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    payload = {"text": mensagem}
    response = requests.post(slack_webhook_url, json=payload)
    if response.status_code != 200:
        print(f"Erro ao enviar notificação para o Slack: {response.status_code} - {response.text}")


# função para ler os valores anteriores do arquivo
def ler_valores_anteriores():
    try:
        with open('valores_anteriores.json', 'r') as arquivo:
            data = json.load(arquivo)
            return data
    except (FileNotFoundError, ValueError):
        return {}


# função para escrever os valores atuais no arquivo
def escrever_valor_anterior(valor):
    with open('valores_anteriores.json', 'w') as arquivo:
        json.dump({'preco': valor}, arquivo)


# main
if __name__ == "__main__":
    try:
        driver.get(url_plataforma)
        time.sleep(5)

        preco_atual = pegar_preco()
        valores_anteriores = ler_valores_anteriores()
        preco_anterior = valores_anteriores.get('preco')

        if preco_anterior is None or preco_atual != preco_anterior:
            enviar_notificacao_slack(f"O preço mudou para R$ {preco_atual}")
            escrever_valor_anterior(preco_atual)

    finally:
        driver.quit()
