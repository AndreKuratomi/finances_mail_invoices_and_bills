import os

from tests.conftest import required_variables


class TestEnvExampleClass:
    def test_whether_env_example_exists(self) -> None:
        if not os.path.exists('.env.example'):
            raise FileNotFoundError("Variable '.env.example' not found!")
        assert os.path.exists('.env.example')


    def test_variables_titles_env_example(self) -> None:
        with open('.env.example', encoding='utf-8') as file:
            env_variables: str = file.read()
            for var in required_variables:
                assert var in env_variables, f"Environment variable {var} is missing in .env.example!"    
