import os

from tests.conftest import gitignore_list


class TestGitignoreClass:
    def test_if_gitignore_exists(self) -> None:
        if not os.path.exists('.gitignore'):
            raise FileNotFoundError("File '.gitignore' not found!")
        assert os.path.exists('.gitignore')

    def test_gitignore_content(self) -> None:
        """Tests whether certain elements exist or not in .gitignore."""
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
                raise FileNotFoundError(f"It wasn't found the items {remained} in .gitignore!")
