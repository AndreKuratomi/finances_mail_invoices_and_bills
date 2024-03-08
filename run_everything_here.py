import os
import sys

import django
import ipdb

from datetime import datetime
from pathlib import Path


# Preparing django to run outside its dir:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'novelis_table_filter_mail_project.settings')
sys.path.append("./dj_project")
django.setup()

from dj_project.filter_tables.views import EmailAttachByTable

from management_before_django.table_managements.scripts import tables_to_db

from robot_sharepoint.modules.robots.robot_to_upload_files import upload_files_to_sharepoint
from robot_sharepoint.modules.robots.robot_for_login_and_download_raw_table import robot_for_raw_table
from robot_sharepoint.modules.robot_utils.join_reports import join_reports

from utils.functions.path_length import do_we_have_spreadsheets
from utils.functions.delete_elements import do_we_have_things_to_delete
from utils.variables.envs import download_directory, username, password, raw_table_directory, sharepoint_for_database_and_upload_url, sharepoint_medicoes_url
from utils.variables.paths import edited_tables_path, raw_tables_path, reports_path
from utils.variables.report_files import not_found_list, sent_list, elements_reports_list, sent_title

root_directory = os.path.dirname(os.path.abspath(__file__))
root_directory = str(root_directory)

# Clean up former final reports:
do_we_have_things_to_delete(reports_path, "relatorio_diario.txt")

# Drafts for deleting edited table after month turn:
delete_me_FLAG = "ME_APAGUE_NA_PRIMEIRA_OPERAÇÃO_DO_MÊS.txt"

if not Path(delete_me_FLAG).exists():
    today = datetime.now().strftime("%d-%m-%Y")
    print(today)
    if today.startswith("01"):
        do_we_have_things_to_delete(raw_tables_path, ".xlsx")
        do_we_have_things_to_delete(edited_tables_path, ".xlsx")
    
    Path(delete_me_FLAG).touch()

do_we_have_table_to_work_with = do_we_have_spreadsheets(raw_tables_path)

if not do_we_have_table_to_work_with:
    print("BAIXANDO PLANILHA DO SHAREPOINT.")
    robot_for_raw_table(username, password, sharepoint_for_database_and_upload_url, raw_tables_path)

try:
    tables_to_db.tables_to_db()
    EmailAttachByTable().post(root_directory)
except Exception as e: 
    print(f"PROCESSO INTERROMPIDO! Error: {e} CONTATAR DEV RESPONSÁVEL \n Mas pode continuar.")
finally: 
    print("ELABORANDO RELATÓRIO FINAL E ENVIANDO.")
    join_reports(not_found_list, sent_list, elements_reports_list, reports_path)
    upload_files_to_sharepoint(username, password, reports_path, sharepoint_for_database_and_upload_url)
    print("PROCESSO ENCERRADO. CHECAR RELATÓRIOS.")
