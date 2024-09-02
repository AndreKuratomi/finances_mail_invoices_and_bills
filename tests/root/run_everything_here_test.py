import os
import sys
import django

import importlib

from django.test import TestCase
from django.conf import settings
from pathlib import Path

from tests.conftest import configure_django_settings

import ipdb


root_app_dir = Path(__file__).parents[2]


class TestRunEverythingHereClass:
    def test_if_file_exists(self) -> None:
        """Temporary built-in file 'tmp_path' creation."""
        run_everything_here_path = root_app_dir / 'run_everything_here.py'
        assert run_everything_here_path.exists() and run_everything_here_path.is_file(), f"File '{run_everything_here_path}' not found!"

    def test_pure_imports(self) -> None:
        assert os, ImportError("Module {os} not found! Verify its instalation.")
        assert sys, ImportError("Module {sys} not found! Verify its instalation.")
        assert django, ImportError("Module {django} not found! Verify its instalation.")


    def test_other_module_imports(self) -> None:
        """Tests all modules imported in 'run_everything_here.py' file, except django view."""
        with open('run_everything_here.py', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line.startswith("from ") and "dj_project" not in line:
                    line = line.split()[1]
                    module = importlib.import_module(line)
                    assert module

    
# class TestDjangoViewImportClass(TestCase):
#     def test_django_view(self, configure_django_settings) -> None:
        
#         settings = configure_django_settings
        
#         try:
#             from dj_project.model_to_email.views import EmailAttachByTable
#             self.assertIsNotNone(EmailAttachByTable)
#         except ImportError:
#             self.fail("Importação falhou! Verificar configuração.")
