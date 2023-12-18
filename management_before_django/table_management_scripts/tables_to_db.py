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

import ipdb


# PATH TO TABLE:
tables_path = Path("../raw_table/")

# PATH TO DB:
database_path = Path("../db/")
db = database_path.joinpath("db_sqlite3.db")

load_dotenv()

# ENVS:
# Keys for login:
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# Input ids:
username_input_id = os.getenv("USER_INPUT_ID")
password_input_id = os.getenv("PASSWORD_INPUT_ID")
hover_selector = os.getenv("HOVER_SELECTOR")
download_selector = os.getenv("DOWNLOAD_SELECTOR")

# Sharepoint URL:
sharepoint_url = os.getenv("SHAREPOINT_URL")

# Download directory:
download_directory = os.getenv("DOWNLOAD_DIRECTORY")


# PLACING TABLE TO WORK WITH WITH SELENIUM ROBOT:
robot_for_sharepoint(username, password, username_input_id, password_input_id, sharepoint_url, download_directory)


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
