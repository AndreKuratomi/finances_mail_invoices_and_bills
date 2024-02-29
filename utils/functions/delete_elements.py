from pathlib import Path

from errors.custom_exceptions import TooManyFilesError

import ipdb


def do_we_have_things_to_delete(path: Path, string_to_end_with: str) -> None:
    """Looks for elements we don't want anymore and them deletes one by one with .unlick() method."""
    do_we_have_elem_to_delete = list(path.iterdir())

    slaughterhouse_jail = [elem for elem in do_we_have_elem_to_delete if str(elem).endswith(string_to_end_with)]

    if len(slaughterhouse_jail) > 0:
        for bye in slaughterhouse_jail:
            bye.unlink()
