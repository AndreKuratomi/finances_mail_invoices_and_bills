from openpyxl import load_workbook

import pandas as pd
from pathlib import Path
from tqdm import tqdm

from errors.custom_exceptions import TooManyFilesError

from management_before_django.table_managements.modules.compare_spreadsheets import compare_spreadsheets

from utils.functions.delete_elements import do_we_have_things_to_delete
from utils.functions.path_length import do_we_have_spreadsheets
from utils.variables.paths import edited_tables_path, raw_tables_path
from utils.variables.envs import sheet

import ipdb


def filter_table_column(path: Path, sheet: str) -> pd.DataFrame:
    """Receives the tables' path, filters it as necessary and inserts it to Pandas dataframe"""

    # Checking path content:
    tables_path_content = list(path.iterdir())  
    tables = list()

    for elem in tables_path_content:
        stringfied_elem = str(elem)
        if stringfied_elem.endswith('.xls') or stringfied_elem.endswith('.xlsx') or stringfied_elem.endswith('.xlsm'):
            tables.append(stringfied_elem)

    if len(tables) == 0:
        raise FileNotFoundError("NO TABLE TO WORK WITH!")
    elif len(tables) > 1:
        raise TooManyFilesError
    
    # Working with it:
    for file in tables_path_content:
        if file.is_file():

            path_to_raw = str(raw_tables_path.resolve() / file.name)
            path_to_edited = str(edited_tables_path.resolve() / file.name)

            path_to_table = str(file)
            if path_to_table.endswith('.xls') or path_to_table.endswith('.xlsx') or path_to_table.endswith('.xlsm'):

                # OPENPYXL TO ADD STATUS COLUMN:
                workbook = load_workbook(data_only=True, filename=path_to_table)
                attempt = workbook.active

                col_names = [col.value for col in attempt[1]]
                # ipdb.set_trace()
                # do_we_have_status = [elem.value for elem in col_names if elem.value = "STATUS"]

                if "STATUS" not in col_names:
                    new_column = attempt.max_column + 1

                    attempt.insert_cols(new_column)
                    attempt.cell(row=1, column=new_column).value = "STATUS"

                    for cell in range(2, attempt.max_row + 1):
                        # print(cell)
                        attempt.cell(row=cell, column=new_column).value = "Não enviado"
                    
                    table_in_edited_table_path = do_we_have_spreadsheets(edited_tables_path)
                    
                    # print("path_to_edited:", path_to_edited)
                    # print("path_to_raw:", path_to_raw)
                    # COMPARE HERE:
                    if table_in_edited_table_path:
                        workbook.save(path_to_raw)
                        workbook.close()
                        # ipdb.set_trace()

                        compare_spreadsheets(path_to_raw, path_to_raw, sheet)
                    
                    else:
                        workbook.save(path_to_edited)
                        workbook.close()

                # Delete no more necessary raw table 
                do_we_have_things_to_delete(raw_tables_path, '.xlsx')

                # OPENPYXL TO ADD STATUS COLUMN:
                # ipdb.set_trace()
                workbook = load_workbook(data_only=True, filename=path_to_edited)
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

                # Drop first row (only for this case!):
                df.drop(0, inplace=True)

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

            else:
                raise Exception('Only .xls, .xlsx, or .xlsm files are supported.')
        else:
            raise Exception("Something went wrong with this file... ")
