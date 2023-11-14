import pylightxl as xl
import pandas as pd

import ipdb

def read_excel_file(file_name: str):
    if file_name.endswith('.xls') or file_name.endswith('.xlsx') or file_name.endswith('.xlsm'):
        # PYLIGHTXL (to deal with procx):
        qwerty = xl.readxl(file_name)
        worksheet = qwerty.ws("CARIACICA")
        data_procx = worksheet.rows

        for_pandas = list()
        for row in data_procx:
            for_pandas.append(row)

        df = pd.DataFrame(for_pandas[1:], columns=for_pandas[0])    
        
        # ipdb.set_trace()
        
        return df
    else:
        raise Exception('Only .xls, .xlsx, or .xlsm files are supported.')
