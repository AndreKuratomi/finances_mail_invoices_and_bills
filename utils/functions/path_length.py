from pathlib import Path

from errors.custom_exceptions import TooManyFilesError

import ipdb


def do_we_have_spreadsheets(path: Path) -> bool:
    """Checks if there are one or more excel tables."""

    dir_content = list(path.iterdir())

    do_we_have_any_spreadsheet = [elem for elem in dir_content if str(elem).endswith('.xlsx')]

    if len(do_we_have_any_spreadsheet) == 1:
        return True
    elif len(do_we_have_any_spreadsheet) > 1:
        raise TooManyFilesError
    else:
        return False
