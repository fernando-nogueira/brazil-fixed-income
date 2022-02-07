import numpy as np
import pandas as pd
import datetime as dt
import os
import math

path = str(os.getcwd()).replace("\\","/")
df = pd.read_excel(path + '/feriados_nacionais.xls')

def truncate(number, decimals=0):
    """
    Returns a value truncated to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor

def anbima_calendar(calendar):
    df_fmt = calendar[0:936]
    lst_calendar = list(df_fmt['Data'])
    lst_calendar_date_fmt = []
    for holiday in lst_calendar:
        lst_calendar_date_fmt.append(holiday.date())
    return lst_calendar_date_fmt

df = anbima_calendar(df)

def working_days(inicial_date, final_date, operation_form = 'buy'):
    if operation_form == 'buy':
        inicial_date = inicial_date + dt.timedelta(days=1)
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
    if final_date in workdays: workdays.remove(final_date)
    return workdays

def anbima_filter(calendar_fmt, workdays):
    for holiday in calendar_fmt:
        if holiday in workdays: workdays.remove(holiday)
    workdays.append('')
    return len(workdays)


def ltn_pu(date1, date2, calendar, pu):
    if date1.weekday() == 4:
        days = anbima_filter(calendar, working_days(date1, date2)) - 1
    else:
        days = anbima_filter(calendar, working_days(date1, date2))
    exponencial_days =  truncate((252/days), 16)
    rate = (1000/pu) ** (exponencial_days) - 1
    return truncate(rate, 4)

def ltn(date1, date2, calendar, rate):
    if date1.weekday() == 4:
        days = anbima_filter(calendar, working_days(date1, date2)) - 1
    else:
        days = anbima_filter(calendar, working_days(date1, date2))
    exponencial_days = truncate(days/252, 16)
    p_u = truncate(1000/(1+rate)**(exponencial_days), 2)
    return p_u


ltn_pu(dt.date(2022,2,4), dt.date(2024,7,1), df, 775.65)

ltn(dt.date(2022, 2, 4), dt.date(2024,7,1), df, 0.1128)

def coupon_dates(date1, date2, calendar):
    lst = []
    if date2.weekday() == 6:
        date2 = date2 + dt.timedelta(days=1)
    elif date2.weekday() == 5:
        date2 = date2 + dt.timedelta(days=2)
    else:
        date2 = date2
    lst.append(date2)     
    while date2 > date1 + dt.timedelta(days=6*30):
        date2 = date2 - dt.timedelta(days= 6*30)
        while date2.day != 1:
            date2 = date2 - dt.timedelta(days=1)
        if date2.weekday() == 6:
            date2 = date2 + dt.timedelta(days=1)
        elif date2.weekday() == 5:
            date2 = date2 + dt.timedelta(days=2)
        else:
            date2 = date2

        for holiday in calendar:
            for index in range(0,len(lst)):
                if lst[index] == holiday:     
                    lst[index] = lst[index] + dt.timedelta(days=1)
                    if lst[index].weekday() == 6:
                        lst[index] = lst[index] + dt.timedelta(days=1)
                    elif lst[index].weekday() == 5:
                        lst[index] = lst[index] + dt.timedelta(days=2)
                    else:
                        lst[index] = lst[index]
        lst.append(date2)
        
    return lst

def coupon_working_days(date1, calendar, lst_coupon_dates):
    lst_coupon_working_days = []
    for data in lst_coupon_dates:
        lst_coupon_working_days.append(anbima_filter(calendar,working_days(date1, data, 'buy')))
    return lst_coupon_working_days

coupon_working_days(dt.date(2022,2,4),df,coupon_dates(dt.date(2022,2,4), dt.date(2031,1,1), df))

def ntn_f(date1, date2, calendar, rate):
    lst_days = coupon_working_days(date1, calendar, coupon_dates(date1, date2, calendar))
    coupon_payments = []
    for num in range(0, len(lst_days)):
        if num == 0:
            exponencial_days = truncate(lst_days[num]/252, 16)
            coupon_payments.append(round(1048.80885/(1+rate) ** exponencial_days,9))
        else:
            exponencial_days = truncate(lst_days[num]/252, 16)
            coupon_payments.append(round(48.80885/(1+rate) ** exponencial_days,9))
    p_u = truncate(sum(coupon_payments), 2)
    return p_u

def ntn_f_pu(date1, date2, calendar, pu):
    lst_days = coupon_working_days(date1, calendar, coupon_dates(date1, date2, calendar))
    coupon_payments = []
     


    i = (coupon_payments/48.80885) ** (dun/252)- 1
    for num in range(0, len(lst_days)):
        if num == 0:
            exponencial_days = truncate(lst_days[num]/252, 16)
            coupon_payments.append(round(1048.80885/(1+rate) ** exponencial_days,9))
        else:
            exponencial_days = truncate(lst_days[num]/252, 16)
            coupon_payments.append(round(48.80885/(1+rate) ** exponencial_days,9))
    p_u = truncate(sum(coupon_payments), 2)