from ..modules.create_model import create_model_from_database
from ..modules.insert_table_to_db import insert_table_to_db
from ..modules.table_columns_edition import filter_table_column

from utils.variables.envs import sheet
from utils.variables.paths import db, edited_tables_path, raw_tables_path

import ipdb


def tables_to_db() -> None:
    """All functions that work from manipulation of table downloaded in 'raw table' till the creation of a django model."""

    # Read Excel file and return it filtered into Dataframe:
    pandas_dataframe = filter_table_column(raw_tables_path, edited_tables_path, sheet)

    insert_table_to_db(db, pandas_dataframe)

    # Create Django model:
    create_model_from_database()
