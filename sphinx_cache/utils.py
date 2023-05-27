from pathlib import Path
from typing import Optional


def check_env_pickle_exist(doctree_dir: Path) -> Optional[bool]:
    """
    Function to check if the `environment.pickle` file is in the `.doctrees` directory

    :param doctree_dir:  path to the `.doctrees` directory
    :return: True or False
    """
    if doctree_dir.exists():
        return doctree_dir.joinpath("environment.pickle") in doctree_dir.iterdir()
    return None
