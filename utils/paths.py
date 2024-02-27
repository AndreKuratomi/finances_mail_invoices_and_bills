from pathlib import Path

database_path = Path("./management_before_django/db/")
db = database_path.joinpath("db_sqlite3.db")

reports_path = Path("./robot_sharepoint/reports/")

raw_tables_path = Path("./management_before_django/raw_table/")
edited_tables_path = Path("./management_before_django/edited_table/")
