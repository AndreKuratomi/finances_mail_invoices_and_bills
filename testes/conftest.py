import os
import django
import pytest
import sys

from django.conf import settings
from typing import List


# BAT:

bat_elements_list: List[str] = ['cd "', r'call ".\venv\Scripts\activate"', 'py rode_tudo_aqui.py ', 'IF %ERRORLEVEL% NEQ 0']


# .ENV:

email_pattern: str = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

link_pattern: str = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'

required_variables: List[str] = [
    "SECRET_KEY", "EMAIL_HOST_USER", "EMAIL_HOST_PASSWORD", "EMAIL_NFE", "SHAREPOINT_FATURAMENTO_URL", 
    "SHAREPOINT_MEDICOES_URL", "DOWNLOAD_DIRECTORY", "RAW_TABLE_DIRECTORY", "SHEET", "SHEET_CONTACTS"
]

txt: str = 'django-insecure-'


# .GITIGNORE:

gitignore_list: List[str] = ["venv/", ".env", "faturamentos_enviados.txt", "faturamentos_nao_encontrados.txt", "*relatorio_diario.txt"]


# REQUIREMENTS.TXT:

dependencies_pattern: str = r'^[a-zA-Z0-9_.-]+==[a-zA-Z0-9_.-]+(\.\d+)*$'

venv_dirs: List[str] = ["Include", "Lib", "Scripts", "share"]

venv_scripts_dir_content: List[str] = ["activate", "activate.bat", "Activate.ps1", "deactivate.bat", "python.exe"]


# VENV:

@pytest.fixture
def get_venv_path() -> str:
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    venv_dir = os.path.join(root_dir, 'venv')

    return venv_dir


# DJANGO:

@pytest.fixture(scope="session") # parameter: executed once per test session rather than once per test case
def configure_django_settings():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finances_table_filter_mail_project.settings')
    sys.path.append("./dj_project")
    django.setup()
    yield settings
