import os

from pathlib import Path
from tests.conftest import venv_dirs, venv_scripts_dir_content
from typing import List

import ipdb


class TestVenvClass:
    def test_if_venv_dir_exists(self) -> None:
        if not os.path.exists('venv/'):
            raise FileNotFoundError("Diretory 'venv/' not found!")
        assert os.path.exists('venv/')


    def test_venv_directories(self, get_venv_path) -> None:
        venv_dir: str = get_venv_path
        dir: Path = Path(venv_dir)

        for folder in dir.iterdir():
            if folder.is_dir():
                # Logic for converting from Path to string and extract element:
                len_venv_dir = len(venv_dir) + 1
                folder = str(folder)
                folder = folder[len_venv_dir:]

                dirs: List[str] = [folder for folder in venv_dirs if folder in venv_dirs]

        assert dirs == venv_dirs, f"Mandatory directory {folder} missing in venv/!"
        
    
    def test_venv_content_dir_script(self, get_venv_path) -> None:
        venv_dir: str = get_venv_path
        dir: Path = Path(venv_dir)

        for folder in dir.iterdir():
            if folder.is_dir():
                # Logic for converting from Path to string and extract directory:
                len_venv_dir = len(venv_dir) + 1
                str_folder = str(folder)
                filtered_str_folder = str_folder[len_venv_dir:]

                if filtered_str_folder == "Scripts":
                    script = list()
                    for elem in folder.iterdir():
                        # Logic for converting from Path to string and extract element:
                        str_folder = str(folder)
                        str_elem = str(elem)
                        len_str_folder_dir = len(str_folder) + 1
                        filtered_str_elem = str_elem[len_str_folder_dir:]

                        if filtered_str_elem in venv_scripts_dir_content:
                            script.append(filtered_str_elem)

                    assert script == venv_scripts_dir_content, f"The directory {filtered_str_folder} is missing some files or contains unexpected files: {set(venv_scripts_dir_content) - set(script)}"
