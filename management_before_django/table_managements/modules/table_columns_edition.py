import pandas as pd
import time

from openpyxl import load_workbook
from pathlib import Path
from tqdm import tqdm

from management_before_django.table_managements.modules.compare_spreadsheets import compare_spreadsheets
from management_before_django.table_managements.modules.take_path_from_directory import paths_with_file_name, paths_com_muitos_nomes_de_arquivos

from utils.functions.path_length import temos_tabelas

import ipdb


def filter_table_column(raw_path: Path, edited_path: Path, sheet: str) -> pd.DataFrame:
    """Receives the tables' path, filters it as necessary and inserts it to Pandas dataframe"""

    (contatos, complete_file_path_to_raw, file_path_to_raw) = paths_com_muitos_nomes_de_arquivos(raw_path)
    # print(contatos)


    # OPENPYXL PARA ADICIONAR COLUNA CONTATOS:
    workbook_contacts_data = load_workbook(data_only=True, filename=contatos)
    contacts_data = workbook_contacts_data['1-Clientes']

    workbook_all_data = load_workbook(data_only=True, filename=file_path_to_raw)
    print(file_path_to_raw)
    all_data = workbook_all_data['2-por cliente']

    nomes_colunas = [col.value for col in all_data[1]]

    if "CONTATOS" not in nomes_colunas:
        nova_coluna = all_data.max_column + 1
        
        all_data.insert_cols(nova_coluna)
        all_data.cell(row=1, column=nova_coluna).value = "CONTATOS"

        # Comparing by CNPJ:
        # for cell in range(2, all_data.max_row):
        for index, all_data_row in enumerate(all_data.iter_rows(min_row=2, values_only=True), start=2):
            for contacts_row in contacts_data.iter_rows(min_row=2, values_only=True):
                contacts_cnpj = contacts_row[4].replace('.', '').replace('/', '').replace('-', '')
                if contacts_cnpj == all_data_row[4]:
                    all_data.cell(row=index, column=nova_coluna).value = contacts_row[7]
                    break
  
        workbook_all_data.save(complete_file_path_to_raw)
 

    # OPENPYXL TO ADD STATUS COLUMN:
    col_names = [col.value for col in all_data[1]]
    # do_we_have_status = [elem.value for elem in col_names if elem.value = "STATUS"]

    if "STATUS" not in col_names:
        new_column = all_data.max_column + 1

        all_data.insert_cols(new_column)
        all_data.cell(row=1, column=new_column).value = "STATUS"

        for cell in range(2, all_data.max_row + 1):
            # print(cell)
            all_data.cell(row=cell, column=new_column).value = "Não enviado"

        table_in_edited_table_path = temos_tabelas(edited_path, 1)

        print("file_path_to_raw:", file_path_to_raw)

        # COMPARE HERE:
        if table_in_edited_table_path:
            print("Yes, we do.")
            (complete_file_path_to_edited, file_path_to_edited) = paths_with_file_name(edited_path)
            print("file_path_to_edited:", file_path_to_edited)
            # Update table just downloaded with column status:
            workbook_all_data.save(file_path_to_raw)
            workbook_all_data.close()

            compare_spreadsheets(file_path_to_raw, file_path_to_edited, complete_file_path_to_edited, sheet)
            # ipdb.set_trace()

        else:
            print("No, we don't.")
            edited_file_path = str(edited_path.resolve() / 'edited_table.xlsx')
            workbook_all_data.save(edited_file_path)
            workbook_all_data.close()


    # OPENPYXL FOR NOW FOR TEST EMAILS:
    (complete_file_path_to_edited, file_path_to_edited) = paths_with_file_name(edited_path)

    workbook = load_workbook(data_only=True, filename=file_path_to_edited)
    table_sheet = workbook[sheet]

    for cell in range(2, table_sheet.max_row + 1):
        if cell % 2 == 0:
            table_sheet.cell(row=cell, column=table_sheet.max_column-1).value = "cleidiane.souza@jcgestaoderiscos.com.br"
        else:
            table_sheet.cell(row=cell, column=table_sheet.max_column-1).value = "andre.kuratomi@jcgestaoderiscos.com.br"
    
    workbook.save(complete_file_path_to_edited)
    workbook.close()
    # ipdb.set_trace()
    # OPENPYXL TO ADD TO PANDAS:
    (complete_file_path_to_edited, file_path_to_edited) = paths_with_file_name(edited_path)

    workbook = load_workbook(data_only=True, filename=file_path_to_edited)
    table_sheet = workbook[sheet]
    # ipdb.set_trace()

    rows = list()

    # First row for titles:
    headers = [cell.value for cell in table_sheet[1]]
    headers = [headers[3], headers[4], headers[6],  headers[10], headers[18], headers[23], headers[24]]

    # Other rows for content:
    for row in tqdm(table_sheet.iter_rows(min_row=2), "Filtering rows by columns D, E, K, S and X..."):
        rows.append([cell.value for i, cell in enumerate(row) if i in [3, 4, 6, 10, 18, 23, 24]]) #IMPROVE

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

