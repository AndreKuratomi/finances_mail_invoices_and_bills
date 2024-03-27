import os

from pathlib import Path


def temos_model(models_path: Path) -> bool:
    if os.path.getsize(models_path) > 0:
        print("YES, WE DO!")
        return True
    else:
        return False
