import urllib.request
import datetime as dt
import os
import pandas as pd

path = os.getcwd()
path = str(os.getcwd()).replace("\\","/")
path = path + '/BondRates'

if dt.date.today().weekday() == 0:
    ytday = dt.date.today() - dt.timedelta(days=3)
else:
    ytday = dt.date.today() - dt.timedelta(days=1)

today_fmt  = ytday.strftime("%Y-%m-%d")
year_fmt = ytday.strftime("%y")
day_fmt = ytday.strftime("%d") 

def portuguese_month(today = ytday):
    dict_abv = {1: 'jan', 2: 'fev', 3:'mar', 4:'abr', 5:'mai', 6:'jun', 
                7: 'jul', 8: 'ago', 9: 'set', 10: 'out', 11: 'nov', 12: 'dez'}
    month = int(today.strftime("%m"))
    return dict_abv[month]

url = f'https://www.anbima.com.br/informacoes/merc-sec/arqs/m{year_fmt}{portuguese_month()}{day_fmt}.xls'

save = f'{path}/BondRatesMining.xls'
urllib.request.urlretrieve(url, save)

df_base = pd.read_excel(f'{path}/BondRates.xlsx')

if df_base['Data'].iloc[len(df_base) - 1] == ytday.strftime("%d/%m/%Y"):
    pass
else: 
    df_ltn = pd.read_excel(save, sheet_name = 'LTN', header = 3)
    df_ltn = df_ltn[['Data de Vencimento', 'Tx. Compra', 'Tx. Venda', 'PU']].dropna()
    df_ltn['Título'] = 'LTN'

    df_lft = pd.read_excel(save, sheet_name = 'LFT', header = 3)
    df_lft = df_lft[['Data de Vencimento', 'Tx. Compra', 'Tx. Venda', 'PU']].dropna()
    df_lft['Título'] = 'LFT'

    df_ntnb = pd.read_excel(save, sheet_name = 'NTN-B', header = 3)
    df_ntnb = df_ntnb[['Data de Vencimento', 'Tx. Compra', 'Tx. Venda', 'PU']].dropna()
    df_ntnb['Título'] = 'NTN-B'

    df_ntnf = pd.read_excel(save, sheet_name = 'NTN-F', header = 3)
    df_ntnf = df_ntnf[['Data de Vencimento', 'Tx. Compra', 'Tx. Venda', 'PU']].dropna()
    df_ntnf['Título'] = 'NTN-F'

    df_new = pd.concat([df_base, df_ltn, df_ntnf, df_lft, df_ntnb]) 
    df_new['Data'] = ytday.strftime("%d/%m/%Y")
    
    df = pd.concat([df_base, df_new])
    
    df = df.set_index('Data')

    df.to_excel('BondRates/BondRates.xlsx')
