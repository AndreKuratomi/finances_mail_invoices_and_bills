import os
import time
import subprocess

from pathlib import Path

import ipdb

def create_model_from_database(path_to_db: Path) -> None:
    # from 'python3 manage.py inspectdb > filter_tables/models.py' to a command:
    command = f'cd ../.. && python3 manage.py inspectdb > filter_tables/models.py'
    os.system(command)
