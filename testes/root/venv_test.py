import os

from pathlib import Path
from testes.conftest import venv_dirs, venv_scripts_dir_content
from typing import List

import ipdb


class TestVenvClass:
    def test_venv_dir_existe(self) -> None:
        if not os.path.exists('venv/'):
            raise FileNotFoundError("Diretório 'venv/' não encontrado!")
        assert os.path.exists('venv/')


    def test_venv_diretorios(self, get_venv_path) -> None:
        venv_dir: str = get_venv_path
        dir: Path = Path(venv_dir)

        for folder in dir.iterdir():
            if folder.is_dir():
                # Lógica para converter de Path para string e extrair elemento:
                len_venv_dir = len(venv_dir) + 1
                folder = str(folder)
                folder = folder[len_venv_dir:]

                dirs: List[str] = [folder for folder in venv_dirs if folder in venv_dirs]

        assert dirs == venv_dirs, f"Diretório obrigatório {folder} ausente em venv/!"
        
    
    def test_venv_conteudo_dir_script(self, get_venv_path) -> None:
        venv_dir: str = get_venv_path
        dir: Path = Path(venv_dir)

        for folder in dir.iterdir():
            if folder.is_dir():
                # Lógica para converter de Path para string e extrair diretório:
                len_venv_dir = len(venv_dir) + 1
                str_folder = str(folder)
                filtered_str_folder = str_folder[len_venv_dir:]

                if filtered_str_folder == "Scripts":
                    script = list()
                    for elem in folder.iterdir():
                        # Lógica para converter de Path para string e extrair elemento:
                        str_folder = str(folder)
                        str_elem = str(elem)
                        len_str_folder_dir = len(str_folder) + 1
                        filtered_str_elem = str_elem[len_str_folder_dir:]
                        # print(filtered_str_elem)
                        if filtered_str_elem in venv_scripts_dir_content:
                            script.append(filtered_str_elem)
                    # ipdb.set_trace()
                    assert script == venv_scripts_dir_content, f"O diretório  tem "


    # def se instalado um mock do venv pode ser alimentado por outro do requirements.txt?
