import os

from testes.conftest import bat_elements_list


class TestBatClass:
    def test_se_arquivo_bat_existe(self) -> None:
        if not os.path.exists('rode_aplicacao_aqui.bat'):
            raise FileNotFoundError("Diretório 'rode_aplicacao_aqui.bat' não encontrado!")
        assert os.path.exists('rode_aplicacao_aqui.bat')
    

    def test_elementos_bat(self) -> None:
        """Testa se certos elementos (como 'cd "') existem no arquivo .bat"""
        with open('rode_aplicacao_aqui.bat') as bat:
            bat_content: str = bat.read()
            for elem in bat_elements_list:
                assert elem in bat_content, f"O elemento '{elem}' não está presente em 'rode_aplicacao_aqui.bat'."
