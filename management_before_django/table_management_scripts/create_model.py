import os
import time
from pathlib import Path

import sys
# sys.path.append("../..")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'novelis_table_filter_mail_project.settings')

import django
from django.core.mail import send_mail
django.setup()

from filter_tables.views import SendEmailView

from tqdm import tqdm

import ipdb

def create_model_from_database() -> None:
    # from 'python3 manage.py inspectdb > filter_tables/models.py' to a command:
    command = f'cd ../.. && python3 manage.py inspectdb > filter_tables/models.py'
    os.system(command)
    # ipdb.set_trace()
    time.sleep(1)  # wait for file to be created

    # Modify the generated model file
    with open("../../filter_tables/models.py", "r") as file:
        lines = file.readlines()

    with open("../../filter_tables/models.py", "w") as file:
        for line in tqdm(lines, "Creating django model from SQLite3..."):
            # print(line)

            if "id = models.IntegerField(blank=True, null=True)" in line:
                file.write(line.replace("id = models.IntegerField(blank=True, null=True)", "id = models.AutoField(primary_key=True)"))
                # print(line)
            else:
                file.write(line)

    # # RUN DJANGO:
    # command = f'cd ../.. && python3 manage.py runserver'
    # os.system(command)

    # time.sleep(1)

    # command = f'cd filter_tables/ && python3 views.py'
    # os.system(command)

    # RUN VIEW SEND EMAIL:
    # print("before")
    SendEmailView().post()
    # print("after")

    # ipdb.set_trace()
