import requests
from bs4 import BeautifulSoup
import json
import re
import pandas as pd
from pandas import json_normalize


def readDatabase(database_id, token, headers):
    url_read = f'https://api.notion.com/v1/databases/{database_id}/query'

    response = requests.post(url_read, headers=headers)

    response_json = response.json()
    
    data = response_json['results']

    for line in data:
        # print(line)
        for campo in line['properties']:
            # print(campo)

            format = line['properties'][campo]['type']
            # print(format)
            #print(line['properties'][campo]['rich_text'])
            # print(line['properties'][campo][format][0])
            try: 
                print(line['properties'][campo][format][0]['text']['content'])
            except: 
                print("campo vazio: " + campo)
    # with open('./output.json', 'w', encoding='utf8') as f:
    #      json.dump(response.json(), f)



def createPage(database_id, headers):

    createUrl = 'https://api.notion.com/v1/pages'

    newPageData = {
        "parent": { "database_id": database_id },
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": "teste"
                        }
                    }
                ]
            },
            "Tags": {
                "rich_text": [
                    {
                        "text": {
                            "content": "Amazing"
                        }
                    }
                ]
            },
            "testando": {
                "rich_text": [
                    {
                        "text": {
                            "content": "Active"
                        }
                    }
                ]
            }
        }
    }

    
    data = json.dumps(newPageData)
    # print(str(uploadData))

    res = requests.request("POST", createUrl, headers=headers, data=data)

    print(res.status_code)
    print(res.text)

def updatePage(page_id, headers, text):
    updateUrl = f"https://api.notion.com/v1/pages/{page_id}"

    updateData = {
        "properties": {
            "testando": {
                "type": "rich_text",
                "rich_text": [
                    {
                        "text": {
                            "content": text
                        }
                    }
                ]
            }
        }        
    }
    

    data = json.dumps(updateData)

    response = requests.patch(updateUrl, headers=headers, data=data)

    print(response.status_code)
    # print(response.text)



with requests.session() as s:

    login_info = {
        'login_email': 'murillo.stein@bixtecnologia.com.br',
        'login_password': 'Murillo8'
    }
    login_url = 'https://app.feedz.com.br/autenticacao/login'

    s.post(login_url, data=login_info)

    # /\ fazer a consulta /\
    page = s.get(
        f'https://app.feedz.com.br/trilhas')
    soup = BeautifulSoup(page.content, 'html.parser')

    # print(soup.pret)

    script = soup.find_all('script', type='text/javascript')

    # print(script)
    array = re.findall(
                '"name": (\".*\")', str(script))
    
    # print(array)
    json_avencer = array[0].replace('"', '')



    li = soup.find_all('li')

    #paragraph = li.find_all('p')

    #print(paragraph)

    # print(json_avencer)
    # notion params
    # https://www.notion.so/d66622662242471b84d44b54000cae41?v=00d15eee35ea450eb3bb1933e957bb7d
    # integration secret_uCplAaGHdcF4X1k6Q4q2Dedt1eves3nGj6aeTUDRnL5
    database_id = 'd66622662242471b84d44b54000cae41'

    token = 'secret_uCplAaGHdcF4X1k6Q4q2Dedt1eves3nGj6aeTUDRnL5'

    headers = {
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }

    # readDatabase(database_id, token, headers)

    page_id = 'f6769b0f-7efc-4fc6-acee-7f089597890f'

    # updatePage(page_id, headers)
    # createPage(database_id, headers)