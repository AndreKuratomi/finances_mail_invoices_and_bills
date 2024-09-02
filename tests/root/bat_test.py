import os

from tests.conftest import bat_elements_list


class TestBatClass:
    def test_if_bat_file_exists(self) -> None:
        if not os.path.exists('run_everything_here.bat'):
            raise FileNotFoundError("Directory 'run_everything_here.bat' not found!")
        assert os.path.exists('run_everything_here.bat')
    

    def test_elements_bat(self) -> None:
        """Tests whether certain elements (as 'cd "') exist in the .bat file"""
        with open('run_everything_here.bat') as bat:
            bat_content: str = bat.read()
            for elem in bat_elements_list:
                assert elem in bat_content, f"The element '{elem}' in not in 'run_everything_here.bat'."
