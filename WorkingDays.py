import pandas as pd
import numpy as np
import os
import datetime as dt

path = os.getcwd()
path = '/Users/user/Desktop/Fernando/RendaFixa'
df = pd.read_excel(path + '/feriados_nacionais.xls')
df_fmt = df[0:936]
all_holiday = list(df_fmt['Data'])

dt.date(2020,1,1) + dt.timedelta(days=1)
dt.date(2022,1,25).weekday() != 6

def working_days(inicial_date, final_date):
    workday = []
    while inicial_date != final_date:
        inicial_date = inicial_date + dt.timedelta(days=1)
        if inicial_date.weekday() != 6 or 7:
            workday.append(inicial_date)
    return workday

# Já conta como se fosse data de liquidação (D+1)
ex =working_days(dt.date(2020,1,1), dt.date(2021,1,1))

all_holiday_fmt = []
for holiday in all_holiday:
    all_holiday_fmt.append(holiday.date())

for holiday in all_holiday_fmt:
    if holiday in ex: ex.remove(holiday)

liquidation_date = len(ex)
buy_date = len(ex) + 1# colocar um dt.timedelta(days=-1), algo assim para já receber o dado direto, tudo depende de como será feito
