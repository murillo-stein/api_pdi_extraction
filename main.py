import pandas as pd
from bs4 import BeautifulSoup
import json
import re
import requests
import pandas as pd

from functions import getProgress
from functions import getPageID
from functions import updatePage

with requests.session() as s:

    # FEEDZs setup
    login_info = {
        'login_email': 'murillo.stein@bixtecnologia.com.br',
        'login_password': 'Murillo8'
    }
    login_url = 'https://app.feedz.com.br/autenticacao/login'
    s.post(login_url, data=login_info)

    page = s.get(
        f'https://app.feedz.com.br/trilhas')
    soup = BeautifulSoup(page.content, 'html.parser')

    # NOTIONs setup
    # https://developers.notion.com/docs/getting-started
    database_id = 'd66622662242471b84d44b54000cae41' # vai na página da tabela, pega a url da página, copia o código que está entre o '/' e o '?v'
    token = 'secret_uCplAaGHdcF4X1k6Q4q2Dedt1eves3nGj6aeTUDRnL5' # token da integração
    headers = {
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }
    url_read = f'https://api.notion.com/v1/databases/{database_id}/query'

    response = requests.post(url_read, headers=headers)
    response_json = response.json()
    data = response_json['results']

    # iterate over captured PDIs
    lista_trilhas = soup.find_all(
        'div', {"class": "fdz-flex-column employee-info employee-list"})

    for item in lista_trilhas:
        try:
            # aqui ele filtra a trilha de desenvolvimento pelo nome dela
            output = re.findall('PDI (.*) - 4º tri 22', str(item))
            if output:
                print(output)

                progress = getProgress(item)
                page_id = getPageID(data, output[0])
                updatePage(page_id, headers, progress)
        except:
            print('não achou')
