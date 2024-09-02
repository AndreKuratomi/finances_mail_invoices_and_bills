from pathlib import Path
from typing import Tuple, List

from errors.custom_exceptions import TooManyFilesError
import ipdb


def paths_with_file_name(path: Path) -> Tuple[str, str]:
    """Takes a path and returns it with its content and its complete path."""

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

    elem_to_work_with = Path(tables[0])

    if elem_to_work_with.is_file():

        complete_path_to_dir = str(path.resolve() / elem_to_work_with.name)

        return (complete_path_to_dir, elem_to_work_with)

    else:
        raise Exception("Something went wrong with this file... ")
    

def paths_with_many_file_names(path: Path) -> Tuple[str, str, str]:
    """Take full path to directory edited_table."""

    # Checking path content:
    tables_path_content = list(path.iterdir())  
    tables = list()

    for elem in tables_path_content:
        stringfied_elem = str(elem)
        if stringfied_elem.endswith('.xls') or stringfied_elem.endswith('.xlsx') or stringfied_elem.endswith('.xlsm'):
            tables.append(elem)

    if len(tables) == 0:
        raise FileNotFoundError("NO TABLE TO WORK WITH!")
    elif len(tables) > 2:
        raise TooManyFilesError

    contacts = ""

    for element_to_work_with in tables:
        if str(element_to_work_with).endswith('.xlsx'): # CONTACTS
            contacts = element_to_work_with
        else:
            outro = element_to_work_with
            complete_path_to_dir = str(path.resolve() / element_to_work_with.name)
    
    return (contacts, complete_path_to_dir, outro)
