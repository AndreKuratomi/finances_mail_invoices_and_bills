from pathlib import Path

from ..modules.create_model import create_model_from_database
from ..modules.table_columns_edition import filter_table_column
from ..modules.insert_table_to_db import insert_table_to_db

import ipdb


# PATH TO TABLE:
# tables_path = Path(".attachments/")
tables_path = Path("./management_before_django/raw_table/")

# PATH TO DB:
database_path = Path("./management_before_django/db/")
db = database_path.joinpath("db_sqlite3.db")


def tables_to_db() -> None:
    """Gathers all table functions from raw table edition till django model creation"""

    # Read Excel file and return it filtered by color into Dataframe:
    pandas_dataframe = filter_table_column(tables_path, "2-por cliente") # HOW TO AUTOMATIZE THIS 2nd PARAMETER???

    # Insert table to SQLite database:
    insert_table_to_db(db, pandas_dataframe)

    # Create Django model
    create_model_from_database()
