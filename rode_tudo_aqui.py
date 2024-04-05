import os
import sys

import django
import ipdb

from pathlib import Path


# Empty models case:
from management_before_django.table_managements.modules.create_model import create_model_from_database
from utils.variables.paths import models_file_path
from utils.functions.temos_model import temos_model

if not temos_model(models_file_path):
    create_model_from_database()

# Preparing django to run outside its dir:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finances_table_filter_mail_project.settings')
sys.path.append("./dj_project")
django.setup()

from dj_project.model_to_email.views import EmailAttachByTable

from management_before_django.table_managements.scripts import tables_to_db

from robot_sharepoint.modules.robots.robot_to_upload_files import upload_files_to_sharepoint
from robot_sharepoint.modules.robots.robot_for_login_and_download_raw_table import robot_for_raw_table
from robot_sharepoint.modules.robots.robo_para_download_contatos import download_contatos_no_sharepoint
from robot_sharepoint.modules.robot_utils.join_reports import join_reports

from utils.functions.path_length import temos_tabelas
from utils.functions.deletar_elementos import temos_algo_para_deletar
from utils.variables.envs import download_directory, user_email, password, raw_table_directory, sharepoint_for_database_and_upload_url, sharepoint_medicoes_url
from utils.variables.paths import edited_tables_path, models_file_path, raw_tables_path, reports_path
from utils.variables.report_files import not_found_list, sent_list, elements_reports_list, sent_title


# Diretório da aplicação para django depois trabalhar com anexos na view:
diretorio_raiz = os.path.dirname(os.path.abspath(__file__))
diretorio_raiz = str(diretorio_raiz)

# Apagar relatório final anterior:
temos_algo_para_deletar(reports_path, "relatorio_diario.txt")

# Rascunhos para deletar tabela editada após virada do mês:
delete_me_FLAG = "ME_APAGUE_ANTES_DA_PRIMEIRA_OPERAÇÃO_DO_MÊS.txt"

if not Path(delete_me_FLAG).exists():
    temos_algo_para_deletar(raw_tables_path, ".xlsx")
    temos_algo_para_deletar(edited_tables_path, ".xlsx")
    
    Path(delete_me_FLAG).touch()
    with open(delete_me_FLAG, 'w') as file:
        file.write("Só me apague quando for a primeira operação do mês...")
    
    # Criação de relatório de envios por CNPJ e NFE:
    with reports_path.joinpath(sent_list).open("w") as file:
        file.write(sent_title)

temos_tabela_para_trabalhar = temos_tabelas(raw_tables_path, 2)

if not temos_tabela_para_trabalhar:
    print("BAIXANDO PLANILHAS DO SHAREPOINT.")
    download_contatos_no_sharepoint(user_email, password, sharepoint_for_database_and_upload_url, raw_tables_path)
    robot_for_raw_table(user_email, password, sharepoint_for_database_and_upload_url, raw_tables_path)

try:
    tables_to_db.tables_to_db()
    EmailAttachByTable().post(diretorio_raiz)
except Exception as e: 
    print(f"PROCESSO INTERROMPIDO! Error: {e} CONTATAR DEV RESPONSÁVEL \n Mas pode continuar.")
finally: 
    print("ELABORANDO RELATÓRIO FINAL E ENVIANDO.")
    join_reports(not_found_list, sent_list, elements_reports_list, reports_path)
    upload_files_to_sharepoint(user_email, password, reports_path, sharepoint_for_database_and_upload_url)
    print("PROCESSO ENCERRADO. CHECAR RELATÓRIOS.")
