import pandas as pd
import datetime as dt
import os

path = str(os.getcwd()).replace("\\","/")
df = pd.read_excel(path + '/feriados_nacionais.xls')

dt.date(2010,1,1) > dt.date(2020,1,1)

def working_days(inicial_date, final_date, operation_form = 'buy'):
    if operation_form == 'buy':
        inicial_date = inicial_date - dt.timedelta(days=1)
    elif operation_form == 'liquidate':
        inicial_date = inicial_date
    if inicial_date > final_date:
        date_cache = inicial_date
        inicial_date = final_date
        final_date = date_cache
    elif inicial_date == final_date:
        return []
    workdays = []
    mon_to_fri = [0, 1, 2, 3, 4]
    while inicial_date != final_date:
        inicial_date = inicial_date + dt.timedelta(days=1)
        day = inicial_date.weekday()
        if day in mon_to_fri:
            workdays.append(inicial_date)  
    return workdays

def anbima_calendar(calendar, workdays):
    df_fmt = calendar[0:936]
    lst_calendar = list(df_fmt['Data'])
    lst_calendar_date_fmt = []
    for holiday in lst_calendar:
        lst_calendar_date_fmt.append(holiday.date())
    for holiday in lst_calendar_date_fmt:
        if holiday in workdays: workdays.remove(holiday)
    return workdays

# Teste
len(anbima_calendar(df, working_days(dt.date(2021,1,1), dt.date(2010,1,1), operation_form='liquidate')))