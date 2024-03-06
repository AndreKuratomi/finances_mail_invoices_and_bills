import os
import stat
import shutil

from pathlib import Path
from tqdm import tqdm

import ipdb


def empty_download_directories(download_dir: str, default_download_dir: str, progress_bar: bool = True) -> None:
    """Check if download dirs have content and if so empty them."""
    
    # VIRTUAL DOWNLOAD DIR:
    if progress_bar:
        pbar1 = tqdm(desc="Check whether virtual directory is empty", total=8)
        pbar1.update(1)
    
    pbar1.update(1)

    dir_to_origin_path = Path(default_download_dir)
    pbar1.update(1)

    origin_dir_content = list(dir_to_origin_path.iterdir())
    pbar1.update(1)

    if len(origin_dir_content) > 0:
        # ipdb.set_trace()
        pbar1.update(1)
        # os.remove(default_download_dir)

        # Windows:
        # Grant default_download_dir read, write and execute permissions:
        os.chmod(default_download_dir, stat.S_IRWXU)
        pbar1.update(1)

        shutil.rmtree(default_download_dir) # very agressive...
        pbar1.update(1)

        os.mkdir(default_download_dir)
        pbar1.update(1)
    pbar1.close()

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
        # ipdb.set_trace()
        slaughterhouse_jail = [elem for elem in destiny_dir_content if str(elem).endswith('.pdf') or str(elem).endswith('.xlsx')]
        pbar1.update(1)
        # ipdb.set_trace()
        if len(slaughterhouse_jail) > 0:
            pbar1.update(1)
            
            for bye in slaughterhouse_jail:
                pbar2.update(1)
                Path(bye).unlink()
        pbar2.update(1)

        # shutil.rmtree(download_dir) # very agressive...
        # pbar2.update(1)

        # os.mkdir(dir_to_destiny_path)
        # pbar2.update(1)

    pbar2.close()


def moving_files_from_virtual_dir(download_dir: str, default_download_dir: str) -> None:
    """...to specific dir."""
    # ipdb.set_trace()
    dir_to_path = Path(default_download_dir)
    dir_content = list(dir_to_path.iterdir())

    for file in tqdm(dir_content, "Moving downloaded files"):
        print("file_to_be_moved_to_dir:", file)
        if file.is_file():
            path_to_table = str(file)
            shutil.move(path_to_table, download_dir)
        else:
            raise Exception("Something went wrong... check the file itself")
