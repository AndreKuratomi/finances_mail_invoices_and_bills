from pathlib import Path

from errors.custom_exceptions import TooManyFilesError

import ipdb


def temos_algo_para_deletar(path: Path, string_para_terminar_com: str) -> None:
    """Procura por elementos que não queremos mais e aí deletamos um por um com o método .unlink()."""
    temos_elemento_para_deletar = list(path.iterdir())

    matadouro = [elem for elem in temos_elemento_para_deletar if str(elem).endswith(string_para_terminar_com)]

    if len(matadouro) > 0:
        for passar_bem in matadouro:
            passar_bem.unlink()
