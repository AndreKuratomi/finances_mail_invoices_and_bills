from datetime import datetime


year = datetime.now().strftime("%Y")
month = datetime.now().strftime("%m")

months_list = ['JANEIRO', 'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO', 'JUNHO', 'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO']
month_number = int(month) - 1
month_name = months_list[month_number]

mes_sharepoint = month + ' ' + month_name
