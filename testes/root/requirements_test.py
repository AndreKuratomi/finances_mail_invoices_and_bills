import os
import re

from testes.conftest import dependencies_pattern


class TestRequirementsClass:
    def test_requirements_existe(self) -> None:
        if not os.path.exists('requirements.txt'):
            raise FileNotFoundError("Arquivo 'requirements.txt' não encontrado!")
        assert os.path.exists('requirements.txt')


    def test_conteudo_requirements(self) -> None:
        with open('requirements.txt') as file:
            env_variables: str = file.read()
            # print(env_variables)
            assert len(env_variables) > 0, "Arquivo 'requirements.txt' vazio!"

    
    def test_formatacao_conteudo_requirements(self) -> None:
        with open('requirements.txt', encoding='utf-16') as file:
            for line in file:
                line = line.strip()
                assert re.match(dependencies_pattern, line), f"A dependência '{line}' não segue o padrão '{dependencies_pattern}'!"
