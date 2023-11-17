import pandas as pd
import pylightxl as xl

from pathlib import Path

import ipdb

def read_excel_file(path: Path, sheet: str):
    tables_path_content = list(path.iterdir())  

    if len(tables_path_content) == 0:
        raise FileNotFoundError("NO TABLE TO WORK WITH!")

    for file in tables_path_content:
        if file.is_file():
            path_to_table = str(file)
            # ipdb.set_trace()
            if path_to_table.endswith('.xls') or path_to_table.endswith('.xlsx') or path_to_table.endswith('.xlsm'):

                # PYLIGHTXL (to deal with procx):
                qwerty = xl.readxl(path_to_table)
                worksheet = qwerty.ws(sheet)
                data_procx = worksheet.rows

                for_pandas = list()
                for row in data_procx:
                    for_pandas.append(row)

                df = pd.DataFrame(for_pandas[1:], columns=for_pandas[0])
                print(df)
                print(df["METAL"])
                
                return df
            else:
                raise Exception('Only .xls, .xlsx, or .xlsm files are supported.')
        else:
            raise Exception("Something went wrong...")
