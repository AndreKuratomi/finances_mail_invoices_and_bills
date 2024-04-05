import os
import sys
import django

import importlib

from django.test import TestCase
from django.conf import settings
from pathlib import Path

from testes.conftest import configure_django_settings

import ipdb


root_app_dir = Path(__file__).parents[2]


class TestRodeTudoAquiClass:
    def test_se_arquivo_existe(self) -> None:
        """Criação de arquivo temporário built-in 'tmp_path'"""
        rode_tudo_aqui_path = root_app_dir / 'rode_tudo_aqui.py'
        assert rode_tudo_aqui_path.exists() and rode_tudo_aqui_path.is_file(), f"Arquivo '{rode_tudo_aqui_path}' não encontrado!"

    def test_pure_imports(self) -> None:
        assert os, ImportError("Module {os} não encontrado! Verificar instalação.")
        assert sys, ImportError("Module {sys} não encontrado! Verificar instalação.")
        assert django, ImportError("Module {django} não encontrado! Verificar instalação.")


    def test_other_module_imports(self) -> None:
        """Testa todos os módulos importados em 'rode_tudo_aqui.py', exceto django view."""
        with open('rode_tudo_aqui.py', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line.startswith("from ") and "dj_project" not in line:
                    line = line.split()[1]
                    module = importlib.import_module(line)
                    assert module

    
class TestDjangoViewImportClass(TestCase):
    def test_django_view(self, configure_django_settings) -> None:
        
        settings = configure_django_settings
        
        try:
            from dj_project.model_to_email.views import EmailAttachByTable
            self.assertIsNotNone(EmailAttachByTable)
        except ImportError:
            self.fail("Importação falhou! Verificar configuração.")
    # def se função temos model funciona
    # def se função create_model_blablabla funciona

    # def se função temos_algo_para_deletar funciona

    # def se criação ME_APAGUE funciona
    # def se criação RELATÓRIO sent_list funciona

    # def se função temos_tabela funciona
    # def se função robo_contatos funciona
    # def se função robo_raw funciona
