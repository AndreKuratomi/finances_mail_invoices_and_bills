import os
import time
import subprocess

from pathlib import Path

import ipdb

def create_model_from_database(path_to_db: Path) -> None:
    # from 'python3 manage.py inspectdb > filter_tables/models.py' to a command:
    command = f'cd ../.. && python3 manage.py inspectdb > filter_tables/models.py'
    os.system(command)

    time.sleep(1)  # wait for file to be created

    # Modify the generated model file
    with open("../../filter_tables/models.py", "r") as file:
        lines = file.readlines()

    with open("../../filter_tables/models.py", "w") as file:
        for line in lines:
            # print(line)

            if "id = models.IntegerField(blank=True, null=True)" in line:
                file.write(line.replace("id = models.IntegerField(blank=True, null=True)", "id = models.AutoField(primary_key=True)"))
                print(line)
            else:
                file.write(line)

    command = f'cd ../.. && python3 manage.py runserver'
    os.system(command)
