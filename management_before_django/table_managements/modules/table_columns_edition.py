from openpyxl import load_workbook

import pandas as pd
from pathlib import Path
from tqdm import tqdm

from errors.custom_exceptions import TooManyFilesError

import ipdb


def filter_table_column(path: Path, sheet: str) -> pd.DataFrame:
    # print(path)
    # ipdb.set_trace()
    """Receives the tables' path, filters it as necessary and inserts it to Pandas dataframe"""
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
    
    for file in tables_path_content:
        if file.is_file():
            path_to_table = str(file)
            if path_to_table.endswith('.xls') or path_to_table.endswith('.xlsx') or path_to_table.endswith('.xlsm'):

                # OPENPYXL:
                workbook = load_workbook(data_only=True, filename=path_to_table)
                table_sheet = workbook[sheet]

                rows = list()

                # First row for titles:
                headers = [cell.value for cell in table_sheet[2]]
                headers = [headers[3], headers[4], headers[6], headers[18]]

                # Other rows for content:
                for row in tqdm(table_sheet.iter_rows(min_row=2), "Filtering rows by columns D, E and S..."):
                    rows.append([cell.value for i, cell in enumerate(row) if i in [3, 4, 6, 18]]) #IMPROVE

                df = pd.DataFrame(rows, columns=headers)

                # Drop first row (only for this case!):
                df.drop(0)

                # Adding column ID to make django work:
                if 'ID' not in df.columns:
                    ID = range(1, df.shape[0]+1)
                    df.insert(0, "id", ID)
                    df.set_index('id')

                # Editing NFE column to hide first character:
                df.loc[1:, 'Numero'] = df.loc[1:, 'Numero'].apply(lambda x : x[1:])

                return df

            else:
                raise Exception('Only .xls, .xlsx, or .xlsm files are supported.')
        else:
            raise Exception("Something went wrong... ")
