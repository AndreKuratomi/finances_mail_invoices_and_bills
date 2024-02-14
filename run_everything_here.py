import os
import sys

import django

import ipdb

# Preparing django to run outside its dir:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'novelis_table_filter_mail_project.settings')
sys.path.append("./dj_project")
django.setup()

from management_before_django.table_managements.scripts import tables_to_db
from dj_project.filter_tables.views import EmailAttachByTable

root_directory = os.path.dirname(os.path.abspath(__file__))
root_directory = str(root_directory)
print(f"root_directory: {root_directory}")
# ipdb.set_trace()
tables_to_db.tables_to_db()

EmailAttachByTable().post(root_directory)
