from datetime import datetime


year = datetime.now().strftime("%Y")
month = datetime.now().strftime("%m")

months_list = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']
month_number = int(month) - 1
month_name = months_list[month_number]

mes_sharepoint = month + ' ' + month_name
