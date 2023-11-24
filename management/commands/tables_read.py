import pandas as pd
import pylightxl as xl

from pathlib import Path

import ipdb

def read_excel_file(edited_table_path: Path, sheet: str):

    tables_path_content = list(edited_table_path.iterdir())  

    if len(tables_path_content) == 0:
        raise FileNotFoundError("NO TABLE TO WORK WITH!")

    for file in tables_path_content:
        if file.is_file():
            path_to_table = str(file)

            # specific_char = "/"
            # index = path_to_table.find(specific_char)
            # path_content = edited_table_path.joinpath(path_to_table[index+1:])

            # PYLIGHTXL (to deal with procx):
            # qwerty = xl.readxl(path_to_table) # FOR FILTERED TABLE!
            qwerty = xl.readxl(file) # FOR FILTERED TABLE!
            worksheet = qwerty.ws(sheet)
            data_procx = worksheet.rows
            # print(data_procx)

            for_pandas = list()
            for row in data_procx:
                print(row)
                for_pandas.append(row)

            df = pd.DataFrame(for_pandas[1:], columns=for_pandas[0])
            ipdb.set_trace()
            
            df = df.iloc[:, 0:14]
            print(df)

            # ORDER BY WHAT?

            if 'ID' not in df.columns:
                ID = range(1, df.shape[0]+1)
                df.insert(0, "id", ID)
                df.set_index('id')

            # print(df)
            print(df["METAL"])
            # print(df.columns)
            
            return df
        
        else:
            raise Exception("Something went wrong...")
