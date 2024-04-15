import pandas as pd
import time

from openpyxl import load_workbook
from pathlib import Path
from tqdm import tqdm

from management_before_django.table_managements.modules.openpyxl_module import adicionar_coluna_contatos, adicionar_coluna_referencia, adicionar_coluna_status, contatos_teste, workbook_para_pandas
from management_before_django.table_managements.modules.paths_module import paths_with_file_name, paths_com_muitos_nomes_de_arquivos

from utils.variables.envs import sheet, sheet_contacts

import ipdb


def filter_table_column(raw_path: Path, edited_path: Path, sheet: str) -> pd.DataFrame:
    """Módulo para trabalhar com todos os scripts que usam openpyxl fornecendo paths e workbooks."""

    # PLANILHAS RECÉM-BAIXADAS:
    # Paths:
    (contatos, complete_file_path_to_raw, file_path_to_raw) = paths_com_muitos_nomes_de_arquivos(raw_path)

    # Workbooks:
    workbook_contacts_data = load_workbook(data_only=True, filename=contatos)
    contacts_data = workbook_contacts_data[sheet_contacts]

    workbook_all_raw_data = load_workbook(data_only=True, filename=file_path_to_raw)
    all_raw_data = workbook_all_raw_data[sheet]

    # Funções Openpyxl:
    adicionar_coluna_contatos(all_raw_data, contacts_data, workbook_all_raw_data, complete_file_path_to_raw)
    adicionar_coluna_referencia(all_raw_data, workbook_all_raw_data, complete_file_path_to_raw)
    adicionar_coluna_status(all_raw_data, edited_path, file_path_to_raw, workbook_all_raw_data, sheet)


    # PLANILHA EDITADA:
    # Paths:
    (complete_file_path_to_edited, file_path_to_edited) = paths_with_file_name(edited_path)

    # Workbooks:
    workbook_all_edited_data = load_workbook(data_only=True, filename=file_path_to_edited)
    all_edited_data = workbook_all_edited_data[sheet]

    # Funções Openpyxl:
    contatos_teste(all_edited_data, workbook_all_edited_data, complete_file_path_to_edited)
    pandas_dataframe = workbook_para_pandas(all_edited_data)

    return pandas_dataframe
