import pandas as pd

from management_before_django.table_managements.modules.take_path_from_directory import paths_with_file_name
from openpyxl import load_workbook
from pathlib import Path
from tqdm import tqdm
from utils.functions.path_length import temos_tabelas

import ipdb


def adicionar_coluna_contatos(all_data, contacts_data, workbook_all_data, complete_file_path_to_raw) -> None:
    """Openpyxl para adicionar coluna 'CONTATOS'."""

    nomes_colunas = [col.value for col in all_data[1]]

    if "CONTATOS" not in nomes_colunas:
        nova_coluna = all_data.max_column + 1
        
        all_data.insert_cols(nova_coluna)
        all_data.cell(row=1, column=nova_coluna).value = "CONTATOS"

        # Comparing by CNPJ:
        for index, all_data_row in enumerate(all_data.iter_rows(min_row=2, values_only=True), start=2):
            for contacts_row in contacts_data.iter_rows(min_row=2, values_only=True):
                contacts_cnpj = contacts_row[4].replace('.', '').replace('/', '').replace('-', '')
                if contacts_cnpj == all_data_row[4]:
                    all_data.cell(row=index, column=nova_coluna).value = contacts_row[7]
                    break
  
        workbook_all_data.save(complete_file_path_to_raw)


def compare_spreadsheets(path_to_raw: str, path_to_edited: str, full_path_to_edited: str, sheet: str) -> None:
    updated_workbook = load_workbook(data_only=True, filename=path_to_raw)
    old_workbook = load_workbook(data_only=True, filename=path_to_edited)

    worksheet = old_workbook.active

    updated_sheet = updated_workbook[sheet]
    old_sheet = old_workbook[sheet]

    updated_data = []
    old_data = []

    # Extract data from updated table
    for row in updated_sheet.iter_rows(min_row=2, values_only=True):
        updated_data.append(row)

    # Extract data from old table
    for row in old_sheet.iter_rows(min_row=2, values_only=True):
        old_data.append(row)
    print("previous_old_data1:", len(old_data))
    print("updated_data:", len(updated_data))
    new_lines = [row for row in updated_data if row[6] not in [old_row[6] for old_row in old_data]]

    if new_lines:
        print("LETS WORK!")
        old_data.extend(new_lines)
        print("new_old_data2:", len(old_data))
        
        for lines in new_lines:
            old_sheet.append(lines)
        
        old_workbook.save(full_path_to_edited)
        old_workbook.close()
    # ipdb.set_trace()
    print("DONE!")


def adicionar_coluna_status(all_data, edited_path, file_path_to_raw, workbook_all_data, sheet) -> None:
    """Openpyxl para adicionar coluna 'STATUS'."""
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
            # Salvando path tabela editada:
            edited_file_path = str(edited_path.resolve() / 'edited_table.xlsx')

            workbook_all_data.save(edited_file_path)
            workbook_all_data.close()


def contatos_teste(table_sheet, workbook, complete_file_path_to_edited) -> None:
    """Openpyxl para alterar contatos para emails teste."""

    for cell in range(2, table_sheet.max_row + 1):
        if cell % 2 == 0:
            table_sheet.cell(row=cell, column=table_sheet.max_column-1).value = "cleidiane.souza@jcgestaoderiscos.com.br"
        else:
            table_sheet.cell(row=cell, column=table_sheet.max_column-1).value = "andre.kuratomi@jcgestaoderiscos.com.br"
    
    workbook.save(complete_file_path_to_edited)
    workbook.close()
    # ipdb.set_trace()


def workbook_para_pandas(table_sheet) -> pd.DataFrame:
    """Da tabela editada acima com Openpyxl para Dataframe Pandas."""

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
    # print(df['Dt Vencto'])

    # Editing date column to show only date in brazilian format:
    df['Dt Vencto'] = pd.to_datetime(df['Dt Vencto'], errors='coerce')
    df['Dt Vencto'] = df['Dt Vencto'].dt.tz_localize('UTC').dt.tz_convert('America/Sao_Paulo')
    df['Dt Vencto'] = (df['Dt Vencto'] + pd.Timedelta(days=1)).dt.strftime('%d/%m/%Y')

    # Attempts to avoid TimeDelta:
    # df['Dt Vencto'] = pd.to_datetime(df['Dt Vencto'], format='%d/%m/%Y', errors='coerce')
    # df['Dt Vencto'] = df['Dt Vencto'].dt.tz_localize('UTC').dt.tz_convert('America/Sao_Paulo')
    # df['Dt Vencto'] = df['Dt Vencto'].dt.strftime('%d/%m/%Y')
    print(df)
    # ipdb.set_trace()
    return df


def status_update(edited_path: Path, row_data: dict) -> None:
    """Receives the tables' path and row_data as dict, searches for the original row by NFE value and if found updates status to 'Enviado'."""

    (complete_file_path_to_edited, file_path_to_edited) = paths_with_file_name(edited_path)

    # OPENPYXL TO ADD STATUS COLUMN:
    workbook = load_workbook(data_only=True, filename=file_path_to_edited)
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
    else:
        try:
            for row_to_update in range(2, worksheet.max_row + 1): 
                like_ancient_nfe = '0' + row_data['nfe']
                if worksheet.cell(row=row_to_update, column=column_index_for_nfe).value == str(like_ancient_nfe):
                    print("row_data['nfe']:", row_data['nfe'])
                    worksheet.cell(row=row_to_update, column=column_index_for_status).value = "Enviado"
                    # ipdb.set_trace()
                    print("worksheet.cell(row=row_to_update, column=column_index_for_status).value:", worksheet.cell(row=row_to_update, column=column_index_for_status).value)
                    break

            workbook.save(complete_file_path_to_edited)
            workbook.close()

        except Exception as e:
            print(e)
            raise FileNotFoundError("No row with this NFE found!")
