import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pandas import DataFrame
from pathlib import Path
import sqlite3

from dotenv import load_dotenv

from create_model import create_model_from_database
from tables_color_edition import filter_table_by_yellow

from robot_sharepoint.robot_to_login_and_download_from_sharepoint import robot_for_sharepoint
from robot_sharepoint.recursive_robot import recursive_robot

import ipdb


# PATH TO TABLE:
tables_path = Path("../raw_table/")

# PATH TO DB:
database_path = Path("../db/")
db = database_path.joinpath("db_sqlite3.db")

load_dotenv()

# ENVS:
# Keys for login:
username = os.getenv("USERN")
# username = "naoresponda@jcgestaoderiscos.com.br"
password = os.getenv("PASSWORD")

# Input ids:
username_input_id = os.getenv("USER_INPUT_ID")
password_input_id = os.getenv("PASSWORD_INPUT_ID")
hover_selector = os.getenv("HOVER_SELECTOR")
download_selector = os.getenv("DOWNLOAD_SELECTOR")
# hover_selector = "div[data-selection-index='1']"
# download_selector = "button[data-automationid='downloadCommand']"

# Sharepoint URL:
sharepoint_url = os.getenv("SHAREPOINT_URL")

# Download directory:
download_directory = os.getenv("DOWNLOAD_DIRECTORY")
# download_directory = "/Users/andre.kuratomi/OneDrive - JC Gestao de Riscos/Área de Trabalho/tables_to_db_mail/tables_to_db_and_mail/management_before_django/raw_table/"
# ipdb.set_trace()

# TAKING INPUT IDS WITH SELENIUM ROBOT:
input_ids = recursive_robot(username, sharepoint_url)
print(input_ids)
# PLACING TABLE TO WORK WITH WITH SELENIUM ROBOT:
robot_for_sharepoint(username, password, input_ids["user_input_id"], input_ids["password_input_id"], hover_selector, download_selector, sharepoint_url, download_directory)


def insert_table_with_procx(db: Path, df: DataFrame) -> None:
    # Connect to SQLite3 database:
    with sqlite3.connect(db) as conn:
        table_name = "table_name"
        df.to_sql(table_name, conn, if_exists='replace', index=True)

# Read Excel file and return it filtered by color into Dataframe:
pandas_dataframe = filter_table_by_yellow(tables_path, "CARIACICA") # HOW TO AUTOMIZE THIS PARAMETER???

# Insert table to SQLite database:
insert_table_with_procx(db, pandas_dataframe)

# Create Django model
create_model_from_database()
