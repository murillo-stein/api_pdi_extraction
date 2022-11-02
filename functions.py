import pandas as pd
from bs4 import BeautifulSoup
import json
import re
import requests
import pandas as pd

def getProgress(all_divs):
    textos = []
    for child in all_divs.children:
        # print(child.text)
        if child.text != "\n":
            textos.append(child.text.replace("\n", ""))

    progress = re.findall('[0-9]%', textos[-1])
    print('pegou progresso', progress)
    return progress[0]

def getPageID(data, name_feedz):
    for line in data:
        # print(line)
        page_id = line['id']

        for campo in line['properties']:
            # print(campo)
            format = line['properties'][campo]['type']
            if campo == 'Nome':
                name_notion = line['properties'][campo][format][0]['text']['content']
                if name_notion == name_feedz:
                    # print('igual')
                    print('pegou id')
                    return page_id

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