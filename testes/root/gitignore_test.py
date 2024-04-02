import os

from testes.conftest import gitignore_list


class TestGitignoreClass:
    def test_se_gitignore_existe(self) -> None:
        if not os.path.exists('.gitignore'):
            raise FileNotFoundError("Arquivo '.gitignore' não encontrada!")
        assert os.path.exists('.gitignore')

    def test_conteudo_gitignore(self) -> None:
        ignored_list = list()
        with open('.gitignore', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line in gitignore_list:
                    ignored_list.append(line)
            if ignored_list == gitignore_list:
                assert ignored_list == gitignore_list
            else:
                set_ignored = set(ignored_list)
                set_gitignore = set(gitignore_list)
                remained = set_gitignore.difference(set_ignored)
                raise FileNotFoundError(f"Não foram encontrados os itens {remained} em .gitignore!")
