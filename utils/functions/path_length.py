from pathlib import Path

from errors.custom_exceptions import TooManyFilesError

import ipdb


def temos_tabelas(path: Path) -> bool:
    """Checa se há uma ou mais tabelas excel."""

    dir_content = list(path.iterdir())

    temos_alguma_tabela = [elem for elem in dir_content if str(elem).endswith('.xlsx')]

    if len(temos_alguma_tabela) == 1:
        return True
    elif len(temos_alguma_tabela) > 1:
        raise TooManyFilesError
    else:
        return False
