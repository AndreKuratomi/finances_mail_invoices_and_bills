from ..modules.compare_spreadsheets import compare_spreadsheets
from ..modules.create_model import create_model_from_database
from ..modules.insert_table_to_db import insert_table_to_db
from ..modules.table_columns_edition import filter_table_column

from robot_sharepoint.modules.robots.robot_for_login_and_download_raw_table import robot_for_raw_table

from utils.functions.path_length import do_we_have_spreadsheets
from utils.variables.envs import sheet, download_directory, download_selector, username, password, sharepoint_medicoes_url
from utils.variables.paths import db, edited_tables_path, raw_tables_path

import ipdb


def tables_to_db() -> None:
    """Gathers all table functions from raw table edition till django model creation."""

    # Read Excel file and return it filtered by color into Dataframe:
    pandas_dataframe = filter_table_column(raw_tables_path, sheet) # HOW TO AUTOMATIZE THIS 2nd PARAMETER???

    table_in_edited_table_path = do_we_have_spreadsheets(edited_tables_path)
    
    # if table_in_edited_table_path:
    #     # updated_dataframe = compare_spreadsheets(pandas_dataframe, edited_tables_path, sheet)
    #     print("Em obras...")    
    #     # # Insert table to SQLite database:
    #     # insert_table_to_db(db, updated_dataframe)
    # else:
    #     # Idem:
    #     insert_table_to_db(db, pandas_dataframe)
    insert_table_to_db(db, pandas_dataframe)

    # Create Django model:
    create_model_from_database()
