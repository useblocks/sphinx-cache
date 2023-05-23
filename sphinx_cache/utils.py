"""Logic for interacting with sphinx-build."""
import os
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
        sphinx_output_log = Path(sphinx_args[-1]).joinpath("sphinx.log")
        try:
            remove_dir_command = ["rm", "-fr", sphinx_args[-1]]
            subprocess.run(remove_dir_command, check=True)
            show(command=["sphinx-build"] + sphinx_args)
            sphinx_build = subprocess.run(sphinx_command, check=True, capture_output=True, encoding="utf-8")
            sphinx_output_log.write_text(sphinx_build.stdout)
            show(context=f"- Sphinx build log saved in {sphinx_output_log}")
            return sphinx_build.returncode
        except subprocess.CalledProcessError as e:
            show(context=f"Command exited with exit code: {e.returncode}", error=True)
            return e.returncode

    return build()


def check_env_pickle_exist(doctreedir: str) -> Optional[bool]:
    """
    Function to check if the `environment.pickle` file is in the `.doctrees` directory

    :param doctreedir:  path to the `.doctrees` directory
    :return: True or False
    """
    doctree_dir = Path(os.path.realpath(doctreedir))  # path to the `.doctrees` directory
    if doctree_dir.exists():
        return doctree_dir.joinpath("environment.pickle") in doctree_dir.iterdir()
    return None


def restore_command_invoked(doctreedir: str, cachedir: str):
    """
    Function to restore contents from the cache directory to the `.doctrees` directory

    :param doctreedir: path to the `.doctrees` directory.
    :param cachedir: path to the `cache` directory.
    """
    doctree_dir = Path(os.path.realpath(doctreedir))
    cache_dir = Path(os.path.realpath(cachedir))

    env_pickle_exist = check_env_pickle_exist(doctreedir)
    if not env_pickle_exist:
        if cache_dir.joinpath("environment.pickle") not in cache_dir.iterdir():
            show(context=f"- ⚠️ Skipped restore cmd - Reason: `environment.pickle` file not found in {cachedir}")
        else:
            try:
                show(context=f"- Restoring `.doctrees` contents from {cachedir} to {doctreedir}...")
                shutil.copytree(
                    cache_dir, doctree_dir, dirs_exist_ok=True
                )  # Copy cache directory to .doctrees directory
                show(context="- ✅ Restoring Done")
            except Exception as e:
                show(context=f"- ❌ Error - Reason: {e}", error=True)
    else:
        show(context=f"- ⚠️ Skipped restore cmd - Reason: `environment.pickle` file exists already in {doctreedir}")


def store_command_invoked(doctreedir: str, cachedir: str):
    """
    Function to store contents from the `.doctrees` directory to the cache directory.

    :param doctreedir: path to the `.doctrees` directory.
    :param cachedir: path to the `cache` directory.
    :return:
    """
    doctree_dir = Path(os.path.realpath(doctreedir))
    cache_dir = Path(os.path.realpath(cachedir))

    env_pickle_exist = check_env_pickle_exist(doctreedir)
    if env_pickle_exist:
        try:
            shutil.rmtree(cachedir, ignore_errors=True)  # Delete old cachedir directory
            show(context=f"- Storing `.doctrees` contents from {doctreedir} to {cachedir}...")
            shutil.copytree(doctree_dir, cache_dir, dirs_exist_ok=True)  # Copy .doctrees directory to cache directory
            show(context="- ✅ Storing Done")
        except Exception as e:
            show(context=f"- ❌ Error - Reason: {e}", error=True)

    else:
        show(context=f"️- ⚠️ Skipped store cmd - Reason: `environment.pickle` file does not exist in {doctreedir}")
