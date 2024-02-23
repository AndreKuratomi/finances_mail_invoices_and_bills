import os
import sys

import django
import ipdb


# Preparing django to run outside its dir:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'novelis_table_filter_mail_project.settings')
sys.path.append("./dj_project")
django.setup()

from dj_project.filter_tables.views import EmailAttachByTable
from management_before_django.table_managements.scripts import tables_to_db
from robot_sharepoint.modules.robot_to_upload_files import upload_files_to_sharepoint
from utils.envs import username_test, password_test, sharepoint_for_upload_url
from utils.paths import reports_path

root_directory = os.path.dirname(os.path.abspath(__file__))
root_directory = str(root_directory)
print(f"root_directory: {root_directory}")
# ipdb.set_trace()

tables_to_db.tables_to_db()

try:
    EmailAttachByTable().post(root_directory)
except Exception as e: 
    print(f"PROCESSO INTERROMPIDO! Error: {e} CONTATAR DEV RESPONSÁVEL \n Mas pode continuar.")
finally: 
    upload_files_to_sharepoint(username_test, password_test, reports_path, sharepoint_for_upload_url)
  