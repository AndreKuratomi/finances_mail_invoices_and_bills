from pathlib import Path
from pandas import DataFrame
import sqlite3

import ipdb


def insert_table_to_db(db: Path, df: DataFrame) -> None:
    """Create and connect to SQLite3 database"""
    with sqlite3.connect(db) as conn:
        table_name = "table_name"
        df.to_sql(table_name, conn, if_exists='replace', index=True)
