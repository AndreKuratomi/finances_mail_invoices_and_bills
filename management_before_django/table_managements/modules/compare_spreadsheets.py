import pandas as pd

from openpyxl import load_workbook
from pathlib import Path
from pandas import DataFrame
from tqdm import tqdm

from utils.variables.paths import edited_tables_path, raw_tables_path

import ipdb


def compare_spreadsheets(path_to_raw: str, path_to_edited: str, sheet: str) -> None:
    # ipdb.set_trace()
    updated_workbook = load_workbook(data_only=True, filename=path_to_raw)
    old_workbook = load_workbook(data_only=True, filename=path_to_edited)

    updated_sheet = updated_workbook[sheet]
    old_sheet = old_workbook[sheet]

    updated_data = []
    old_data = []

    # Extract data from updated table
    for row in updated_sheet.iter_rows(min_row=2, values_only=True):
        updated_data.append(row)

    # Extract data from old table
    for row in old_sheet.iter_rows(min_row=2, values_only=True):
        old_data.append(row)

    new_lines = [row for row in updated_data if row[6] not in [old_row[6] for old_row in old_data]]

    if new_lines:
        last_row_index = len(old_data) + 2
        for new_row in new_lines:
            old_sheet.append(new_row)

    old_workbook.save(path_to_edited)
    print("DONE!")
