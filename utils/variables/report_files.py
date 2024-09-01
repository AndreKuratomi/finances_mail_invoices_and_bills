import datetime

current = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

# Raw text files:
elements_reports_list = f"{current}-daily_report.txt"
not_found_list = "billings_not_found.txt"
sent_list = "billings_sent.txt"

# Report titles:
not_found_title = "billings not found: \n"
sent_title = "billings sent: \n"
