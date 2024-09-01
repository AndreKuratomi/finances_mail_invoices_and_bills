import tqdm
import zipfile

from pathlib import Path

from errors.custom_exceptions import TooManyFilesError

import ipdb

def unzipfile(zip_path: str) -> None:
    """Transforms path to zip file and unzips it in the same directory."""

    attachment_path_content = list(Path(zip_path).iterdir())  
        
    for file in tqdm(attachment_path_content, "Unzipping files if zip..."):
        if file.is_file():
            path_to_table = str(file)
            if path_to_table.endswith('.zip'):
                with zipfile.ZipFile(path_to_table, 'r') as zip_ref:
                    zip_ref.extractall(zip_path)
            else:
                continue
        else: 
            raise Exception("No file to work with... Check it out!")
