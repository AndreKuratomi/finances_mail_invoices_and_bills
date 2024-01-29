import os
import time
from pathlib import Path

from tqdm import tqdm

import ipdb

def create_model_from_database() -> None:
    # from 'python3 manage.py inspectdb > filter_tables/models.py' to a command:

    # Paths:
    script_absolute_path = Path(__file__).resolve() # absolute path from computer to here
    django_project_path = script_absolute_path.parents[2] / 'dj_project'
    models_file_path = django_project_path / 'filter_tables' / 'models.py'

    # Linux:
    # command = f'cd ../.. && python3 manage.py inspectdb > filter_tables/models.py'

    # Windows
    command = f'cd {django_project_path} && py manage.py inspectdb > {models_file_path}'
    # command = f'cd ../.. && py manage.py inspectdb > filter_tables/models.py'
    
    os.system(command)
    # ipdb.set_trace()

    time.sleep(1)  # wait for file to be created

    # Modify the generated model file
    with open(f"{models_file_path}", "r") as file:
    # with open("../../filter_tables/models.py", "r") as file:
        lines = file.readlines()

    # Edit model content: 
    with open(f"{models_file_path}", "w") as file:
    # with open("../../filter_tables/models.py", "w") as file:
        for line in tqdm(lines, "Editing django model from SQLite3..."):
            # print(line)

            if "id = models.IntegerField(blank=True, null=True)" in line:
                file.write(line.replace("id = models.IntegerField(blank=True, null=True)", "id = models.AutoField(primary_key=True)"))
                # print(line)
            elif "class Meta:" in line:
                file.write(line)
                file.write("        app_label = 'filter_tables'\n")
            else:
                file.write(line)
