from operator import itemgetter

import pandas as pd
from pandas import DataFrame
from pathlib import Path

import pylightxl as xl

import ipdb

from tables_color_edition import filter_table_by_yellow

# tables_path = Path("./raw_table/")
# df = filter_table_by_yellow(tables_path, "CARIACICA")


def read_excel_file(tables_path: Path, sheet: str):
# def read_excel_file(pd_df: DataFrame):
    # print(dataframe)
    # dataframe_to_list = dataframe.values.tolist()

    tables_path_content = list(tables_path.iterdir())  

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
                # print(row)
                for_pandas.append(row)

            df = pd.DataFrame(for_pandas[1:], columns=for_pandas[0])
            
            df = df.iloc[:, 0:14]
            print(df)

            # ORDER BY WHAT?

            if 'ID' not in df.columns:
                ID = range(1, df.shape[0]+1)
                df.insert(0, "id", ID)
                df.set_index('id')

            print(df)
            # ipdb.set_trace()
            print(df["METAL"])
            # print(df.columns)

            return df


            # # Sorting the two lists:
            # data_procx_sorted = sorted(data_procx, key=lambda x: (int(x) if x.isdigit() else x, itemgetter(3, 4, 5, 7, 8, 9, 10, 11, 12)(x)))
            # dataframe_to_list_sorted = sorted(dataframe_to_list, key=lambda x: (int(x) if x.isdigit() else x, itemgetter(3, 4, 5, 7, 8, 9, 10, 11, 12)(x)))

            # for row1, row2 in zip(data_procx_sorted, dataframe_to_list_sorted):
            #     print("row1: {}".format(row1))
            #     print("row2: {}".format(row2))
                # GUAMBIARRA
            #     if row1[3] == row2[3] and row1[4] == row2[4] and row1[5] == row2[5] and row1[7] == row2[7] and row1[8] == row2[8] and row1[9] == row2[9] and row1[10] == row2[10] and row1[11] == row2[11] and row1[12] == row2[12]:
            #         print('let`s move')
            #         for_pandas.append(row2[6])
            # ipdb.set_trace()

            # dataframe["METAL"] = for_pandas
        
        else:
            raise Exception("Something went wrong...")
        
    # # temp_file_path = "./filtered_table/temp.xlsm"
    # # DOES NOT WORK FOR NOW BECAUSE IT SAVES A CORRUPTED FILE:
    # # pd_df.to_excel(temp_file_path, sheet_name='Sheet1')

    # # PYLIGHTXL (to deal with procx):
    # qwerty = xl.readxl(temp_file_path) # FOR FILTERED TABLE!
    # worksheet = qwerty.ws('Sheet1')
    # data_procx = worksheet.rows
    # # print(data_procx)

    # for_pandas = list()
    # for row in data_procx:
    #     # print(row)
    #     for_pandas.append(row)

    # df = pd.DataFrame(for_pandas[1:], columns=for_pandas[0], dtype=str)
    
    # df = df.iloc[:, 0:14]
    # print(df)
    # ipdb.set_trace()

    # # ORDER BY WHAT?

    # if 'ID' not in df.columns:
    #     ID = range(1, df.shape[0]+1)
    #     df.insert(0, "id", ID)
    #     df.set_index('id')

    # # print(df)
    # print(df["METAL"])
    # # print(df.columns)
    
    # return df


    # for file in tables_path_content:
    #     if file.is_file():
    #         path_to_table = str(file)

    #         # specific_char = "/"
    #         # index = path_to_table.find(specific_char)
    #         # path_content = edited_table_path.joinpath(path_to_table[index+1:])
    #     else:
    #         raise Exception("Something went wrong...")
