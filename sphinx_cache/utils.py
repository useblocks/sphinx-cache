"""Logic for interacting with sphinx-build."""

import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

from sphinx_cache.logging import show


def get_builder(sphinx_args: List[str]) -> int:
    """
    Prepare the function that calls sphinx-build.
    :param sphinx_args: List object containing sphinx build arguments
    :return: Sphinx Build subprocess return code
    """
    sphinx_command = [sys.executable, "-m", "sphinx"] + sphinx_args

    def build() -> int:
        """Generate the documentation using ``sphinx-build``."""

        try:
            remove_dir_command = ["rm", "-fr", sphinx_args[-1]]
            subprocess.run(remove_dir_command, check=True)
            show(command=["sphinx-build"] + sphinx_args)
            sphinx_build = subprocess.run(sphinx_command, check=True)
            return sphinx_build.returncode
        except subprocess.CalledProcessError as e:
            show(context=f"Command exited with exit code: {e.returncode}", error=True)
            return e.returncode

    return build()


def check_env_pickle_exist(doctreedir: Path) -> Optional[bool]:
    """
    Function to check if the `environment.pickle` file is in the `.doctrees` directory

    :param doctreedir:  path to the `.doctrees` directory
    :return: True or False
    """
    doctree_dir = doctreedir  # path to the `.doctrees` directory
    if doctree_dir.exists():
        return doctree_dir.joinpath("environment.pickle") in doctree_dir.iterdir()
    return None


def restore_command_invoked(doctreedir: Path, cachedir: Path):
    """
    Function to restore contents from the cache directory to the `.doctrees` directory

    :param doctreedir: path to the `.doctrees` directory.
    :param cachedir: path to the `cache` directory.
    """
    env_pickle_exist = check_env_pickle_exist(doctreedir)
    if not env_pickle_exist:
        try:
            shutil.copytree(cachedir, doctreedir, dirs_exist_ok=True)  # Copy cache directory to .doctrees directory
            show(context="- ✅Done")
        except Exception as e:
            show(context=f"- ❌Error - Reason: {e}", error=True)
    else:
        show(context=f"- ⚠️`environment.pickle` file exists already in {doctreedir}")


def store_command_invoked(doctreedir: Path, cachedir: Path):
    """
    Function to store contents from the `.doctrees` directory to the cache directory.

    :param doctreedir: path to the `.doctrees` directory.
    :param cachedir: path to the `cache` directory.
    :return:
    """
    env_pickle_exist = check_env_pickle_exist(doctreedir)
    if env_pickle_exist:
        try:
            shutil.rmtree(cachedir, ignore_errors=True)  # Delete old cachedir directory
            shutil.copytree(doctreedir, cachedir, dirs_exist_ok=True)  # Copy .doctrees directory to cache directory
            show(context="- ✅Done")
        except Exception as e:
            show(context=f"- ❌Error - Reason: {e}", error=True)

    else:
        show(context=f"️- ⚠️`environment.pickle` file exists already in {doctreedir}")
