from openpyxl import load_workbook, Workbook
import pandas as pd
from pathlib import Path

import ipdb
import os

# PATH TO RAW TABLE:
tables_path = Path("./raw_table/")

# PATH TO FILTERED TABLE:
filtered_tables_path = Path("./filtered_table/")

# DOES NOT WORK FOR NOW BECAUSE IT SAVES A CORRUPTED FILE:
def filter_table_by_yellow(path: Path, sheet: str):

    tables_path_content = list(path.iterdir())  

    if len(tables_path_content) == 0:
        raise FileNotFoundError("NO TABLE TO WORK WITH!")
    
    for file in tables_path_content:
        if file.is_file():
            path_to_table = str(file)
            if path_to_table.endswith('.xls') or path_to_table.endswith('.xlsx') or path_to_table.endswith('.xlsm'):

                # Edit the character lerolero:
                specific_char = "/"
                index = path_to_table.find(specific_char)
                path_content = path.joinpath(path_to_table[index+1:])

                # OPENPYXL (to deal with colors):
                workbook = load_workbook(filename=path_content)
                table_sheet = workbook[sheet]
                # data = sheet.values

                # First row and all rows with yellow cells in colors list and changes saved:
                new_sheet = workbook.create_sheet('filtered_sheet')
                # wb = new_sheet.active

                # print(table_sheet[1])

                new_sheet.append([cell.value for cell in table_sheet[1]])

                for row in table_sheet.iter_rows(min_row=2):
                    if any(cell.fill.start_color.rgb == 'FFFFFF00' for cell in row):
                        new_sheet.append([cell.value for cell in row])
                
                df = pd.DataFrame(new_sheet.values)
                # ipdb.set_trace()

                return df

                # # Saving in a specific folder:
                # this_project_path_for_saving = '/filtered_table'
                # machine_path = os.getcwd()

                # full_path_for_saving = machine_path + this_project_path_for_saving

                # to_string_again = str(file)

                # if to_string_again.endswith('.xls'):
                #     workbook.save(full_path_for_saving + '/table_renewed.xls')
                # elif to_string_again.endswith('.xlsx'):
                #     workbook.save(full_path_for_saving + '/table_renewed.xlsx')
                # elif to_string_again.endswith('.xlsm'):
                #     workbook.save(full_path_for_saving + '/table_renewed.xlsm')
                #     # workbook.save('table_renewed.xlsm')
                #     print("FILE SAVED!")

            else:
                raise Exception('Only .xls, .xlsx, or .xlsm files are supported.')
        else:
            raise Exception("Something went wrong...")
