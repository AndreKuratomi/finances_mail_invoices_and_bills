import os
import re

from tests.conftest import dependencies_pattern


class TestRequirementsClass:
    def test_if_requirements_exist(self) -> None:
        if not os.path.exists('requirements.txt'):
            raise FileNotFoundError("File 'requirements.txt' not found!")
        assert os.path.exists('requirements.txt')


    def test_requirements_content(self) -> None:
        with open('requirements.txt') as file:
            env_variables: str = file.read() # Python handles encoding automatically because it reads the entire file.
            assert len(env_variables) > 0, "File 'requirements.txt' empty!"

    
    def test_requirements_content_format(self) -> None:
        with open('requirements.txt', encoding='utf-16') as file: # But here as Python reads line by line individually it needs explicit encoding.
            for line in file:
                line = line.strip()
                assert re.match(dependencies_pattern, line), f"The dependnecy '{line}' is not following the pattern '{dependencies_pattern}'!"
