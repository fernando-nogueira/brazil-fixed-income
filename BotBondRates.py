"""
# Importando as bibliotecas
import urllib.request
from datetime import date
import datetime as dt
import os

# Especificando o diretório que será trabalhado (pasta em que o arquivo.py está presente)
path = os.getcwd()
path_ima = path + '\\Dados_IMA'
path_di = path + '\\Dados_DI'

# Criamos as variáveis, que serão usadas como a checagem da criação de pastas e nomeação de arquivos
umDia = dt.timedelta(1)
tresDias = dt.timedelta(3)
hoje = date.today()
if hoje.strftime('%A') == "Monday":
   hoje = date.today() - tresDias
else:
    hoje = date.today() - umDia 
hojeData = hoje.strftime("%Y%m%d")
mesAtual = hoje.strftime("%m")
anoAtual = hoje.strftime("%Y")

# Criando as pastas, se no caso ela não existir
# Checa se a pasta do ano existe, se não existir, cria
pastaAno = f'{path_ima}/{anoAtual}'
if not os.path.exists(pastaAno):
    os.makedirs(pastaAno)

# Checa se a pasta do mês existe, se não existir, cria
pastaMes = f'{path_ima}/{anoAtual}/{mesAtual}'
if not os.path.exists(pastaMes):
    os.makedirs(pastaMes)
    
# Baixando os dados diários do IMA
siteAnbima = "https://www.anbima.com.br/informacoes/ima/arqs/ima_completo.xls"
saveAnbima = f'{pastaMes}/IMA_{hojeData}.xls'
if not os.path.exists(saveAnbima):
    urllib.request.urlretrieve(siteAnbima, saveAnbima)

################################################################################

# Checa se a pasta do ano existe, se não existir, cria
pastaAno = f'{path_di}/{anoAtual}'
if not os.path.exists(pastaAno):
    os.makedirs(pastaAno)

# Checa se a pasta do mês existe, se não existir, cria
pastaMes = f'{path_di}/{anoAtual}/{mesAtual}'
if not os.path.exists(pastaMes):
    os.makedirs(pastaMes)
    
# Baixando os dados diários do IMA
siteAnbima = "https://www.anbima.com.br/informacoes/est-termo/CZ-down.asp"
saveAnbima = f'{pastaMes}/DI_{hojeData}.xls'
if not os.path.exists(saveAnbima):
    urllib.request.urlretrieve(siteAnbima, saveAnbima)
"""

import urllib.request
import datetime as dt
import os

path = os.getcwd()
path = str(os.getcwd()).replace("\\","/")
path = path + '/VNA'

ytday = dt.date.today() - dt.timedelta(days=1)
today_fmt  = ytday.strftime("%Y-%m-%d")
year_fmt = ytday.strftime("%y")
day_fmt = ytday.strftime("%d") 
day_fmt

def portuguese_month(today = ytday):
    dict_abv = {1: 'jan', 2: 'fev', 3:'mar', 4:'abr', 5:'mai', 6:'jun', 
                7: 'jul', 8: 'ago', 9: 'set', 10: 'out', 11: 'nov', 12: 'dez'}
    month = int(today.strftime("%m"))
    return dict_abv[month]

url = f'https://www.anbima.com.br/informacoes/merc-sec/arqs/m{year_fmt}{portuguese_month()}{day_fmt}.xls'

save = f'BondRatesBZ{today_fmt}.xls'
if not os.path.exists(save):
    urllib.request.urlretrieve(url, save)

