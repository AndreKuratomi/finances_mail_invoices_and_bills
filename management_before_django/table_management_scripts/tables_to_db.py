import os
from pathlib import Path

from dotenv import load_dotenv

from .create_model import create_model_from_database
from .table_columns_edition import filter_table_column
from .insert_table_to_db import insert_table_to_db
# from robot_sharepoint.robot_for_outlook_selenium import robot_for_outlook
# from robot_sharepoint.recursive_robot import recursive_robot_for_outlook

import ipdb


# PATH TO TABLE:
tables_path = Path("./management_before_django/raw_table/")
# tables_path = Path("../raw_table/")

# PATH TO DB:
database_path = Path("./management_before_django/db/")
# database_path = Path("../db/")
db = database_path.joinpath("db_sqlite3.db")

load_dotenv()

# ENVS:
# Keys for login:
username = os.getenv("USER_OUTLOOK")
password = os.getenv("USER_OUTLOOK_PASSWORD")
# print(password)

# Input ids:
hover_selector = os.getenv("HOVER_SELECTOR")
download_selector = os.getenv("DOWNLOAD_SELECTOR")

# Outlook URL:
outlook_url = os.getenv("OUTLOOK_URL")

# Download directory:
download_directory = os.getenv("DOWNLOAD_DIRECTORY")
# download_directory = "/Users/andre.kuratomi/OneDrive - JC Gestao de Riscos/Área de Trabalho/tables_to_db_mail/tables_to_db_and_mail/management_before_django/raw_table/"

def tables_to_db() -> None:
    # # TAKING INPUT IDS WITH SELENIUM ROBOT:
    # input_ids = recursive_robot_for_outlook(username, outlook_url)
    # print(input_ids)

    # # PLACING TABLE TO WORK WITH WITH SELENIUM ROBOT:
    # robot_for_outlook(username, password, input_ids["user_input_id"], input_ids["password_input_id"], hover_selector, download_selector, outlook_url, download_directory)


    # Read Excel file and return it filtered by color into Dataframe:
    pandas_dataframe = filter_table_column(tables_path, "2-por cliente") # HOW TO AUTOMATIZE THIS 2nd PARAMETER???

    # Insert table to SQLite database:
    insert_table_to_db(db, pandas_dataframe)

    # Create Django model
    create_model_from_database()
