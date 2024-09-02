import os
import re

from django.conf import settings
from django.test import TestCase

from pathlib import Path
from tests.conftest import email_pattern, link_pattern, required_variables, txt

import ipdb

root_app_dir = Path(__file__).parents[2]


class TestDotEnvClass:
    # .ENV:
    def test_whether_env_file_exists(self) -> None:
        dotenv_path = root_app_dir / '.env'
        assert dotenv_path.is_file(), f"File '{dotenv_path}' not found!"


    def test_variables_titles_env(self) -> None:
        with open('.env', encoding='utf-8') as file:
            env_variables: str = file.read()
            for var in required_variables:
                assert var in env_variables, f"Environment variable {var} is missing in .env!"

    # SECRET_KEY:
    def test_secret_key_env_format(self) -> None:
        """Test if the variable begins with 'django-insecure-'."""
        with open('.env', encoding='utf-8') as file:
            env_variables: str = file.read()
            for var in required_variables:
                if var == 'SECRET_KEY':
                    assert txt in env_variables, f"Environment variable {var} doesn't begin with the universal format '{txt}'!"
    

    def test_45_characteres(self) -> None:
        with open('.env', encoding='utf-8') as file:
            env_variables: str = file.read()
            for var in required_variables:
                if var == 'SECRET_KEY':
                    env = re.search(rf'{var}=(.*?)\n', env_variables)
                    secret_key_value = env.group(1)
                    assert len(secret_key_value) >= 45, f"Environment variable {var} has not enought length: {len(secret_key_value)}!"


    def test_secret_key_django_validation(self, configure_django_settings) -> None: # DOESN'T REALLY WORK PROPERLY
        """Tests whether variable 'secret_key' can or can't be configured in settings.py."""
        
        settings = configure_django_settings

        with open('.env', encoding='utf-8') as file:
            env_variables: str = file.read()
            for var in required_variables:
                if var == 'SECRET_KEY':
                    env = re.search(rf'{var}=(.*?)\n', env_variables)
                    secret_key_value = env.group(1).strip('"')

                    settings.configure(SECRET_KEY=secret_key_value)
                    assert settings.SECRET_KEY == secret_key_value, f"Environment variable {var} falhou na aplicação da "

    # EMAILS:
    def test_envs_emails_validation(self) -> None:
        """Tests whether the variables EMAIL_HOST_USER and EMAIL_NFE are emails."""
        with open('.env', encoding='utf-8') as file:
            env_variables: str = file.read()
            for var in required_variables:
                if var == 'EMAIL_HOST_USER' or var == 'EMAIL_NFE':
                    env: str = re.search(rf'{var}=(.*?)\n', env_variables)
                    env_value: str = env.group(1).strip('"')
                    assert re.match(email_pattern, env_value) is not None

    # LINKS:
    def test_envs_links(_validationself) -> None:
        """Tests whether the variables SHAREPOINT_BILLINGS_URL and SHAREPOINT_MEASUREMENTS_URL are links."""
        with open('.env', encoding='utf-8') as file:
            env_variables: str = file.read()
            for var in required_variables:
                if var == 'SHAREPOINT_BILLINGS_URL' or var == 'SHAREPOINT_MEASUREMENTS_URL':
                    env = re.search(rf'{var}=(.*?)\n', env_variables)
                    env_value = env.group(1).strip('"')
                    assert re.match(link_pattern, env_value)
