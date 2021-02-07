import pandas as pd
import requests as rq
from bs4 import BeautifulSoup
url = 'https://dataexplorer.ogm.utah.gov/?keyName=TRS&keyValue=04S%2001W%2011&keyType=String&detailXML=SecDetails.xml&DETAILSONLY=True'
response = rq.get(url)
# print(response.text)
print()
print(response.content)
soup = BeautifulSoup(response.content, 'html.parser')
print(soup)