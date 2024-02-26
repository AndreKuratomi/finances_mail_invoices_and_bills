from ..modules.create_model import create_model_from_database
from ..modules.table_columns_edition import filter_table_column
from ..modules.insert_table_to_db import insert_table_to_db

from robot_sharepoint.modules.robot_for_login_and_download_raw_table import robot_for_raw_table

from utils.envs import download_directory, download_selector, username, password, sharepoint_url
from utils.paths import db, tables_path

import ipdb


def tables_to_db() -> None:
    """Gathers all table functions from raw table edition till django model creation."""

    # Elaborate a conditional to check whether there is a table inside raw_table
    # if so, doesn't use this robot.
    # if does, use it.
    
    # robot_for_raw_table(
    #     username,
    #     password,
    #     sharepoint_url,
    #     download_directory,
    # )

    # Read Excel file and return it filtered by color into Dataframe:
    pandas_dataframe = filter_table_column(tables_path, "2-por cliente") # HOW TO AUTOMATIZE THIS 2nd PARAMETER???

    # Insert table to SQLite database:
    insert_table_to_db(db, pandas_dataframe)

    # Create Django model
    create_model_from_database()
