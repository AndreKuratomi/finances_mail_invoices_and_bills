import os
import time

from pathlib import Path
from tqdm import tqdm

import ipdb


def create_model_from_database() -> None:
    """Creates django model from SQLite3 database with inspectdb and adjusts it to suit for django."""

    # Paths:
    script_absolute_path = Path(__file__).resolve() # absolute path from computer to here
    django_project_path = script_absolute_path.parents[3] / 'dj_project'
    models_file_path = django_project_path / 'filter_tables' / 'models.py'
    # From 'python3 manage.py inspectdb > filter_tables/models.py' to a command:
    # Linux:
    # command = f'cd ../.. && python3 manage.py inspectdb > filter_tables/models.py'

    # Windows
    command = f'cd {django_project_path} && py manage.py inspectdb > {models_file_path}'
    
    os.system(command)

    time.sleep(1)  # wait for file to be created

    # Modify the generated model files:
    with open(f"{models_file_path}", "r") as file:
        lines = file.readlines()

    # Edit model content: 
    with open(f"{models_file_path}", "w") as file:
        for line in tqdm(lines, "Editing django model from SQLite3..."):

            if "id = models.IntegerField(blank=True, null=True)" in line:
                file.write(line.replace("id = models.IntegerField(blank=True, null=True)", "id = models.AutoField(primary_key=True)"))
            elif "class Meta:" in line:
                file.write(line)
                file.write("        app_label = 'filter_tables'\n")
            else:
                file.write(line)
