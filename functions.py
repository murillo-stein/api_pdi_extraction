import pandas as pd
from bs4 import BeautifulSoup
import json
import re
import requests
import pandas as pd

def getProgress(all_divs):
    """
    Get the progress of PDI. 
    Args:
        all_divs: beautifulsoup object with the content of divs of the PDI
    Returns:
        A string with the percentage of progress of the PDI
    """
    textos = []
    for child in all_divs.children:
        if child.text != "\n":
            textos.append(child.text.replace("\n", ""))

    progress = re.findall('[0-9]%', textos[-1]) # o progresso esta localizado no ultimo item de cada div
    return progress[0]

def getPageID(data, name_feedz):
    """
    Capture the ID of the line that contains the name of collaborator
    Args:
        data: full content of table
        name_feedz: name of collaborator
    Returns:
        The ID of the line that contains the name of collaborator
    """

    for line in data:
        page_id = line['id']
        for campo in line['properties']:
            format = line['properties'][campo]['type']
            if campo == 'Nome':
                name_notion = line['properties'][campo][format][0]['text']['content']
                if name_notion == name_feedz:
                    return page_id

def updatePage(page_id, headers, text):
    """
    Update the value of a row. It gets the page ID and susbtitute the current value of a specific column.
    Args:
        page_id: id of the line of the table
        headers: inputs for PATCH request 
        text: new value        
    """
    updateUrl = f"https://api.notion.com/v1/pages/{page_id}"
    update_data = {
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
    data = json.dumps(update_data)
    response = requests.patch(updateUrl, headers=headers, data=data)
    print(response.status_code)