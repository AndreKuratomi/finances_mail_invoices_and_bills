from pathlib import Path

database_path = Path("./management_before_django/db/")
db = database_path.joinpath("db_sqlite3.db")

reports_path = Path("./robot_sharepoint/reports/")

raw_tables_path = Path("./management_before_django/raw_table/")
edited_tables_path = Path("./management_before_django/edited_table/")

# models:
script_absolute_path = Path(__file__).resolve() # absolute path from computer to here
django_project_path = script_absolute_path.parents[2] / 'dj_project'
models_file_path = django_project_path / 'model_to_email' / 'models.py'
