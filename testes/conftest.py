import os
import pytest

from typing import List


dependencies_pattern: str = r'^[a-zA-Z0-9_.-]+==[a-zA-Z0-9_.-]+(\.\d+)*$'

email_pattern: str = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

gitignore_list: List[str] = ["venv/", ".env", "faturamentos_enviados.txt", "faturamentos_nao_encontrados.txt", "*relatorio_diario.txt"]

link_pattern: str = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'

required_variables: List[str] = [
    "SECRET_KEY", "EMAIL_HOST_USER", "EMAIL_HOST_PASSWORD", "EMAIL_NFE", "SHAREPOINT_FATURAMENTO_URL", 
    "SHAREPOINT_MEDICOES_URL", "DOWNLOAD_DIRECTORY", "RAW_TABLE_DIRECTORY", "SHEET", "SHEET_CONTACTS"
]

venv_dirs: List[str] = ["Include", "Lib", "Scripts", "share"]

venv_scripts_dir_content: List[str] = ["activate", "activate.bat", "Activate.ps1", "deactivate.bat", "python.exe"]

txt: str = 'django-insecure-'


@pytest.fixture
def get_venv_path() -> str:
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    venv_dir = os.path.join(root_dir, 'venv')
    # ipdb.set_trace()
    print(venv_dir)
    return venv_dir