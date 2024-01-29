import os
import sys

import django
# from django.conf import settings

# Preparing django to run outside its dir:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'novelis_table_filter_mail_project.settings')
sys.path.append("./dj_project")
django.setup()

from management_before_django.table_management_scripts import tables_to_db
from dj_project.filter_tables.views import EmailAttachByTable


tables_to_db.tables_to_db()

EmailAttachByTable().post()
