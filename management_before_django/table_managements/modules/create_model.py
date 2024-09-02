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
    models_file_path = django_project_path / 'model_to_email' / 'models.py'
    
    # From 'python3 manage.py inspectdb > model_to_email/models.py' to a command:
    # Linux:
    # command = f'cd ../.. && python3 manage.py inspectdb > model_to_email/models.py'

    # Windows
    command = f'cd {django_project_path} && py manage.py inspectdb > {models_file_path}'
    os.system(command)

    time.sleep(1)  # wait for file to be created

    # Modify the generated model files:
    with open(f"{models_file_path}", "r") as file:
        lines = file.readlines()

    updated_lines = []
    for line in tqdm(lines, "Editing django model from SQLite3..."):

        if "id = models.IntegerField(blank=True, null=True)" in line:
            updated_lines.append(line.replace("id = models.IntegerField(blank=True, null=True)", "id = models.AutoField(primary_key=True)"))
        elif "class Meta:" in line:
            updated_lines.append(line)
            updated_lines.append("        app_label = 'model_to_email'\n")
        else:
            updated_lines.append(line)
    
    # Edit model content directly: 
    with open(f"{models_file_path}", "w") as file:
        file.writelines(updated_lines)

        # Ensure file is flushed and changes are committed before proceeding
        file.flush()
        os.fsync(file.fileno())

