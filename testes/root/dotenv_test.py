import os
import re

from django.conf import settings
from django.test import TestCase

from pathlib import Path
from testes.conftest import email_pattern, link_pattern, required_variables, txt

import ipdb

root_app_dir = Path(__file__).parents[2]


class TestDotEnvClass:
    # .ENV:
    def test_se_env_existe(self) -> None:
        dotenv_path = root_app_dir / '.env'
        assert dotenv_path.is_file(), f"Arquivo '{dotenv_path}' não encontrado!"


    def test_titulos_variaveis_env(self) -> None:
        with open('.env', encoding='utf-8') as file:
            env_variables: str = file.read()
            for var in required_variables:
                assert var in env_variables, f"Variável de ambiente {var} está faltando em .env!"

    # SECRET_KEY:
    def test_formatacao_secret_key_env(self) -> None:
        """Testa se variável se inicia com 'django-insecure-'."""
        with open('.env', encoding='utf-8') as file:
            env_variables: str = file.read()
            for var in required_variables:
                if var == 'SECRET_KEY':
                    assert txt in env_variables, f"Variável de ambiente {var} não se inicia no formato universal '{txt}'!"
    

    def test_45_caracteres(self) -> None:
        with open('.env', encoding='utf-8') as file:
            env_variables: str = file.read()
            for var in required_variables:
                if var == 'SECRET_KEY':
                    env = re.search(rf'{var}=(.*?)\n', env_variables)
                    secret_key_value = env.group(1)
                    assert len(secret_key_value) >= 45, f"Variável de ambiente {var} não tem uma extenção suficiente: {len(secret_key_value)}!"


    def test_validacao_secret_key_django(self, configure_django_settings) -> None: # NÃO FUNCIONA PROPRIAMENTE
        """Teste se variável SECRET_KEY pode ou não ser configurada em settings.py."""
        
        settings = configure_django_settings

        with open('.env', encoding='utf-8') as file:
            env_variables: str = file.read()
            for var in required_variables:
                if var == 'SECRET_KEY':
                    env = re.search(rf'{var}=(.*?)\n', env_variables)
                    secret_key_value = env.group(1).strip('"')

                    settings.configure(SECRET_KEY=secret_key_value)
                    assert settings.SECRET_KEY == secret_key_value, f"Variável de ambiente {var} falhou na aplicação da "

    # EMAILS:
    def test_validacao_envs_emails(self) -> None:
        """Testa se as variáveis EMAIL_HOST_USER e EMAIL_NFE são emails."""
        with open('.env', encoding='utf-8') as file:
            env_variables: str = file.read()
            for var in required_variables:
                if var == 'EMAIL_HOST_USER' or var == 'EMAIL_NFE':
                    env: str = re.search(rf'{var}=(.*?)\n', env_variables)
                    env_value: str = env.group(1).strip('"')
                    assert re.match(email_pattern, env_value) is not None

    # LINKS:
    def test_validacao_envs_links(self) -> None:
        """Testa se as variáveis SHAREPOINT_FATURAMENTO_URL e SHAREPOINT_MEDICOES_URL são links."""
        with open('.env', encoding='utf-8') as file:
            env_variables: str = file.read()
            for var in required_variables:
                if var == 'SHAREPOINT_FATURAMENTO_URL' or var == 'SHAREPOINT_MEDICOES_URL':
                    env = re.search(rf'{var}=(.*?)\n', env_variables)
                    env_value = env.group(1).strip('"')
                    assert re.match(link_pattern, env_value)
