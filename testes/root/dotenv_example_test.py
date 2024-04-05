import os

from testes.conftest import required_variables


class TestEnvExampleClass:
    def test_env_example_existe(self) -> None:
        if not os.path.exists('.env.example'):
            raise FileNotFoundError("Variável '.env.example' não encontrada!")
        assert os.path.exists('.env.example')


    def test_titulos_variaveis_env_example(self) -> None:
        with open('.env.example', encoding='utf-8') as file:
            env_variables: str = file.read()
            for var in required_variables:
                assert var in env_variables, f"Variável de ambiente {var} está faltando .env.example!"    
