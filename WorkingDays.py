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

# Cálculo dos títulos
# Pré fixados

# Exponencial de dias  OK
# P.U. OK

def ltn(date1, date2, calendar, rate):
    days = anbima_filter(calendar, working_days(date1, date2))
    exponencial_days = truncate(days/252, 14)
    p_u = truncate(1000/(1+rate)**(exponencial_days), 2)
    return p_u

def ltn_pu(date1, date2, calendar, pu):
    if date1.weekday() == 4:
        days = anbima_filter(calendar, working_days(date1, date2)) - 1
    else:
        days = anbima_filter(calendar, working_days(date1, date2))
    exponencial_days =  truncate((252/days), 16)
    rate = (1000/pu) ** (exponencial_days) - 1
    return truncate(rate, 4)

ltn(dt.date(2022, 2, 7), dt.date(2024,7,1), df, 0.1118)
ltn_pu(dt.date(2022,2,7), dt.date(2024,7,1), df, 777.63)
# Juros semestrais - OK
# Exponencial de dias OK
# P.U. OK
# Round nos cupons descontados

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


def lft(date1, date2, calendar, rate, v_n_a):
    days = anbima_filter(calendar, working_days(date1, date2))
    cotation = 100/(1+rate) ** (days/252)
    p_u = truncate((cotation/100), 6) * v_n_a
    p_u = truncate(p_u, 2)
    return p_u

lft(dt.date(2022,2,14), dt.date(2024,9,1), df, 0.0656/100, 11358.735837 * (1+0.1065) ** (1/252))

def ntn_b(date1, date2, calendar, rate, vna):
    lst_days = coupon_working_days(date1, calendar, coupon_dates(date1, date2, calendar))
    coupon_payments = []
    for num in range(0, len(lst_days)):
        if num == 0:
            exponencial_days = truncate(lst_days[num]/252, 16)
            coupon_payments.append(round(102.956301/(1+rate) ** exponencial_days,9))
        else:
            exponencial_days = truncate(lst_days[num]/252, 16)
            coupon_payments.append(round(2.956301/(1+rate) ** exponencial_days,9))
    cotation = truncate(sum(coupon_payments) / 100, 6)
    p_u = truncate(cotation * vna, 2)
    return p_u

ntn_b(dt.date(2022,2,14), dt.date(2055, 5, 15),df, 5.67/100, 3809.882294)


# Como pegar dados do FATOR Acumulado da SELIC, pela internet
# Paramos o código por aqui, nas préfixadas e voltamos quando tivermos acesso as VNA's dos títulos pós-fixados

day_2 = dt.date(2031,1,1)
day_1 = dt.date(2022,2,1)     
ield = 0.1122  
ntn_f(day_1, day_2, df,ield)     
# 945,68


ltn(dt.date(2022, 2, 1), dt.date(2024, 7,1), df, 0.1147)
# 771,51



lft(dt.date(2022,2,1), dt.date(2027,3,1), df, 0.2210/100 ,truncate(11318.981220*(1.0915) ** (1/252), 16))

anbima_filter(df, working_days(dt.date(2021,12,15), dt.date(2022,1,15)))
def ntn_b(date1, date2, calendar, rate, v_n_a):
    days = anbima_filter(calendar, working_days(date1, date2))
    cotation = 100/(1+rate) ** (days/252)
    p_u = truncate((cotation/100), 6) * v_n_a
    p_u = truncate(p_u, 2)
    return p_u
 

 # certo 
10 (exclusive) / 21 (exclusive)

3801.295980 * (1.0069)**(1/22) # certo
ntn_b(dt.date(2022,2,1), dt.date(2035,5,15), df, 5.59/100 , 3802.2235)
1851.54
# Para cada mês, a anbima tem duas projeções, uma antes do dia 15 e uma pós o dia 15
# Utilizei a do mês anterior 0.69 foi a projeção de dezembro, são 22 dias entre o dia 15 de jan e dia 15 de dez
# e acruei apenas um dia pois já peguei o do dia no site da Anbima
3804.858111

3011.56/(79.19/100)
(1.0055) ** x = 0.0004364139385752974
(1.0088) ** (2/22) - 1
(3802.9549185503224/3801.295980)-1
$ 3.011,56
#       while len(set(calendar).intersection(set(lst))) ==
#>>> S2 = set(L2)
#>>> S1.intersection(S2)
#set([2])
## Daqui até aqui a NTN-F
"""
def datas_sem_anbima(date1, date2):
    lst = []
    while date2 > date1 + dt.timedelta(days=6*30):
        date2 = date2 - dt.timedelta(days= 6*30)
        while date2.day != 1:
            date2 = date2 - dt.timedelta(days=1)
        if date2.weekday() == 4:
            date2 = date2 + dt.timedelta(days=1)
        elif date2.weekday() == 3:
            date2 = date2 + dt.timedelta(days=2)
        else:
            date2 = date2
        lst.append(date2)
    
    return lst
"""
"""
def datas_sem_anbima_sem_feriado(date1, date2):
    lst = []
    while date2 > date1 + dt.timedelta(days=6*30):
        date2 = date2 - dt.timedelta(days= 6*30)
        while date2.day != 1:
            date2 = date2 - dt.timedelta(days=1)
        lst.append(date2)
    
    return lst
"""
#ok = datas_sem_anbima(day_1, day_2)
#jyg = datas_sem_anbima_sem_feriado(day_1, day_2)


calendar = df 
df_fmt = calendar[0:936]
lst_calendar = list(df_fmt['Data'])
lst_calendar_date_fmt = []
for holiday in lst_calendar:
    lst_calendar_date_fmt.append(holiday.date())

y = x(day_1,day_2, lst_calendar_date_fmt)
y
z = []
for data in y:
    
    z.append(anbima_calendar(df,working_days(day_1, data, 'liquidate')))

z
ield = 0.1122
beta = []
for num in range(0,len(z)):
    if num == 0:
        beta.append(round(1048.80885/(1+ield) ** ((z[num])/252),9))
    else:
        beta.append(round(48.80885/(1+ield) ** ((z[num])/252),9))
    
round(sum(beta),2)
## Daqui até aqui a NTN-F

# Liquidate funciona para esssa função, por que não tira um dia que nem o buy (bate com o paper do tesouro)


# falta apenas colocar em função



x = anbima_calendar(df,working_days(day_1,day_2,'buy'))
x
len(x)


len(anbima_calendar(df,working_days(dt.date(2021,12,15), dt.date(2024,8,15), operation_form='liquidate')))

# Teste
len(anbima_calendar(df, working_days(dt.date(2021,1,1), dt.date(2010,1,1), operation_form='liquidate')))