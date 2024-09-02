import os
import stat
import shutil

from pathlib import Path
from tqdm import tqdm
from typing import List

import ipdb


def empty_download_directories(download_dir: str, progress_bar: bool = True) -> None:
    """Check if download dirs have content and if so empty them."""

    # DESTINATION DOWNLOAD DIR:
    if progress_bar:
        pbar2 = tqdm(desc="Check whether directory is empty", total=6)
        pbar2.update(1)

    dir_to_destiny_path = Path(download_dir)
    pbar2.update(1)

    destiny_dir_content = list(dir_to_destiny_path.iterdir())
    pbar2.update(1)
    print("destiny_dir_content:", destiny_dir_content)

    if len(destiny_dir_content) > 0:
        pbar2.update(1)
        slaughterhouse = [elem for elem in destiny_dir_content if elem.name != '__init__.py']
        pbar2.update(1)

        if len(slaughterhouse) > 0:
            pbar2.update(1)
            
            for bye in slaughterhouse:
                pbar2.update(1)
                Path(bye).unlink()
        pbar2.update(1)

    pbar2.close()


def moving_files_from_virtual_dir(default_download_dir: str, download_dir: str, files_list: List[str]) -> None:
    """
        Files downloaded from sharepoint to diretory 'default_download_dir' moved to 'download_dir' according to 'files_list' content.
    """

    dir_to_path = Path(default_download_dir)
    dir_content = list(dir_to_path.iterdir())

    for file in tqdm(dir_content, "Moving downloaded files"):
        if file.is_file():
            base_name = os.path.basename(str(file))
            if base_name in files_list:
                path_to_table = str(file)
                shutil.move(path_to_table, download_dir)
        else:
            continue
