from pandas import DataFrame
from pathlib import Path
import sqlite3

from create_model import create_model_from_database
from tables_read_and_turn_to_pandas import read_excel_file
# from tables_color_edition import filter_table_by_yellow

import ipdb

# PATH TO TABLE:
tables_path = Path("./raw_table/")

# PATH TO FILTERED TABLE:
filtered_tables_path = Path("./filtered_table/")

# PATH TO DB:
database_path = Path("./db/")
db = database_path.joinpath("db_sqlite3.db")


def insert_table_with_procx(db: Path, df: DataFrame) -> None:

    # Connect to SQLite3 database:
    with sqlite3.connect(db) as conn:
        table_name = "table_name"
        df.to_sql(table_name, conn, if_exists='replace', index=True)

# Read Excel file and return it filtered by color:
# DOES NOT WORK FOR NOW BECAUSE IT SAVES A CORRUPTED FILE:
# filter_table_by_yellow(tables_path, "CARIACICA") # HOW TO AUTOMIZE THIS PARAMETER???
# pandas_dataframe = filter_table_by_yellow(tables_path, "CARIACICA") # HOW TO AUTOMIZE THIS PARAMETER???

# Read Excel file into Dataframe:
dataframe = read_excel_file(tables_path, "CARIACICA") # HOW TO AUTOMATIZE THIS PARAMETER???

# Insert table to SQLite database:
insert_table_with_procx(db, dataframe)

create_model_from_database(db)
