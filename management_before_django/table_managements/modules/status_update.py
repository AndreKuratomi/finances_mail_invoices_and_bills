from openpyxl import load_workbook

import pandas as pd
from pathlib import Path
from tqdm import tqdm

from errors.custom_exceptions import TooManyFilesError
from utils.variables.paths import edited_tables_path

import ipdb


def status_update(path: Path, row_data: dict) -> None:
    """Receives the tables' path and row_data as dict, searches for the original row by NFE value and if found updates status to 'Enviado'."""

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
            path_to_table = str(file)
            if path_to_table.endswith('.xls') or path_to_table.endswith('.xlsx') or path_to_table.endswith('.xlsm'):

                # OPENPYXL TO ADD STATUS COLUMN:
                workbook = load_workbook(data_only=True, filename=path_to_table)
                worksheet = workbook.active

                # Find column index for NFE ('Numero'):
                column_index_for_nfe = None
                column_index_for_status = None

                for cell in worksheet[1]:
                    # print("cell.value:", cell.value)
                    if cell.value == 'Numero':
                        # ipdb.set_trace()
                        column_index_for_nfe = cell.column
                        # print("cell.column:", cell.column)
                        # print(column_index)
                    elif cell.value == "STATUS":
                        column_index_for_status = cell.column

                if column_index_for_nfe is None or column_index_for_status is None:
                    raise ValueError("Column 'Numero' not found in the worksheet")

                try:
                    for row_to_update in range(2, worksheet.max_row + 1): 
                        like_ancient_nfe = '0' + row_data['nfe']
                        if worksheet.cell(row=row_to_update, column=column_index_for_nfe).value == str(like_ancient_nfe):
                            print("row_data['nfe']:", row_data['nfe'])
                            worksheet.cell(row=row_to_update, column=column_index_for_status).value = "Enviado"
                            # ipdb.set_trace()
                            print("worksheet.cell(row=row_to_update, column=column_index_for_status).value:", worksheet.cell(row=row_to_update, column=column_index_for_status).value)
                            break
                        path_back = str(edited_tables_path.resolve() / file.name)
                        print("path_back:", path_back)

                    workbook.save(path_back)
                    workbook.close()
                    
                except Exception as e:
                    raise FileNotFoundError("No row with this NFE found!")
                    print(e)

        else:
            raise Exception("Something went wrong with this file... ")
