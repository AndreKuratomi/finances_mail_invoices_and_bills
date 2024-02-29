import datetime

current = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")

# Raw text files:
elements_reports_list = f"{current} - relatorio diário.txt"
not_found_list = "faturamentos_nao_encontrados.txt"
sent_list = "faturamentos_enviados.txt"

# Report titles:
not_found_title = "Faturamentos não encontrados: \n"
sent_title = "Faturamentos enviados: \n"
