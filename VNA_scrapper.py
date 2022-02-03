"""
from urllib.request import urlopen, Request
from urllib.parse import urlencode
import urllib.request
from datetime import date
import datetime as dt
import os
"""

from bs4 import BeautifulSoup
import requests
from datetime import date
import os
import pandas as pd

path = os.getcwd()
path = str(os.getcwd()).replace("\\","/")
path = path + '/VNA'
url = "https://www.anbima.com.br/informacoes/vna/vna.asp"

def vna_formatting_data(url, id = "NTN-B"):
    if id == "NTN-B":
        index = 0
    elif id == "LFT":
        index = 3
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')

    lst = str(soup.find_all('tr', attrs={'style':'background-color:white;'})[index])
    v_n_a = float(lst.split(' ')[3].replace('<td>', '').replace('</td>', '').replace('.','').replace(',','.'))
    if id == "NTN-B":
        ipca_projection = float(lst.split(' ')[4].replace('<td>', '').replace('</td>', '').replace(',','.'))
        return [v_n_a, ipca_projection]
    elif id == "LFT":
        selic = float(lst.split(' ')[4].replace('<td>', '').replace('</td>', '').replace(',','.'))
        return [v_n_a, selic]

vna_ntnb = vna_formatting_data(url)
vna_lft = vna_formatting_data(url, 'LFT')
today = date.today().strftime("%d/%m/%Y")

df = pd.read_excel(f'{path}/VNA.xlsx')
if df['Data'].iloc[len(df) - 1] == today:
    pass
else:
    df = df.append({'Data': today, 
                    'VNA NTN-B': vna_ntnb[0],
                    'VNA LFT': vna_lft[0],
                    'IPCA': vna_ntnb[1],
                    'SELIC': vna_lft[1]} ,ignore_index=True)
    df = df.set_index('Data')
    df.to_excel('VNA/VNA.xlsx')