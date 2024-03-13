import pandas as pd
import time

from openpyxl import load_workbook
from pathlib import Path
from tqdm import tqdm

from management_before_django.table_managements.modules.compare_spreadsheets import compare_spreadsheets
from management_before_django.table_managements.modules.take_path_from_directory import paths_with_file_name

from utils.functions.path_length import temos_tabelas

import ipdb


def filter_table_column(raw_path: Path, edited_path: Path, sheet: str) -> pd.DataFrame:
    """Receives the tables' path, filters it as necessary and inserts it to Pandas dataframe"""

    (complete_file_path_to_raw, file_path_to_raw) = paths_with_file_name(raw_path)

    # OPENPYXL TO ADD STATUS COLUMN:

    workbook = load_workbook(data_only=True, filename=file_path_to_raw)
    attempt = workbook.active

    col_names = [col.value for col in attempt[1]]
    # do_we_have_status = [elem.value for elem in col_names if elem.value = "STATUS"]

    if "STATUS" not in col_names:
        new_column = attempt.max_column + 1

        attempt.insert_cols(new_column)
        attempt.cell(row=1, column=new_column).value = "STATUS"

        for cell in range(2, attempt.max_row + 1):
            # print(cell)
            attempt.cell(row=cell, column=new_column).value = "Não enviado"

        table_in_edited_table_path = temos_tabelas(edited_path)

        print("file_path_to_raw:", file_path_to_raw)

        # COMPARE HERE:
        if table_in_edited_table_path:
            print("Yes, we do.")
            (complete_file_path_to_edited, file_path_to_edited) = paths_with_file_name(edited_path)
            print("file_path_to_edited:", file_path_to_edited)
            # Update table just downloaded with column status:
            workbook.save(file_path_to_raw)
            workbook.close()

            compare_spreadsheets(file_path_to_raw, file_path_to_edited, complete_file_path_to_edited, sheet)
            # ipdb.set_trace()

        else:
            print("No, we don't.")
            edited_file_path = str(edited_path.resolve() / 'edited_table.xlsx')
            workbook.save(edited_file_path)
            workbook.close()

    # OPENPYXL TO ADD STATUS COLUMN:
    (complete_file_path_to_edited, file_path_to_edited) = paths_with_file_name(edited_path)

    workbook = load_workbook(data_only=True, filename=file_path_to_edited)
    table_sheet = workbook[sheet]
    # ipdb.set_trace()

    rows = list()

    # First row for titles:
    headers = [cell.value for cell in table_sheet[1]]
    headers = [headers[3], headers[4], headers[6],  headers[10], headers[18], headers[23]]

    # Other rows for content:
    for row in tqdm(table_sheet.iter_rows(min_row=2), "Filtering rows by columns D, E, K, S and X..."):
        rows.append([cell.value for i, cell in enumerate(row) if i in [3, 4, 6, 10, 18, 23]]) #IMPROVE

    # PANDAS!
    df = pd.DataFrame(rows, columns=headers)

    # # Drop first row (only for this case!):
    # df.drop(0, inplace=True)

    # Adding column ID to make django work:
    if 'ID' not in df.columns:
        ID = range(1, df.shape[0]+1)
        df.insert(0, "id", ID)
        df.set_index('id')

    # Editing NFE column to hide first character:
    df['Numero'] = df['Numero'].apply(lambda x : x[1:])

    # Editing date column to show only date in brazilian format:
    df['Dt Vencto'] = pd.to_datetime(df['Dt Vencto'], errors='coerce')
    df['Dt Vencto'] = df['Dt Vencto'].dt.tz_localize('UTC').dt.tz_convert('America/Sao_Paulo')
    df['Dt Vencto'] = df['Dt Vencto'].dt.strftime('%d/%m/%Y')
    print(df)

    return df

