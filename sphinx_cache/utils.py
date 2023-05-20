"""Logic for interacting with sphinx-build."""

import shlex
import subprocess
import sys
import shutil
from typing import List, Tuple

from pathlib import Path

from sphinx_cache.logging import show

SPHINX_BUILD_OPTIONS = (
    ("b", "builder"),
    ("a", None),
    ("E", None),
    ("d", "path"),
    ("j", "N"),
    ("c", "path"),
    ("C", None),
    ("D", "setting=value"),
    ("t", "tag"),
    ("A", "name=value"),
    ("n", None),
    ("v", None),
    ("q", None),
    ("Q", None),
    ("w", "file"),
    ("W", None),
    ("T", None),
    ("N", None),
    ("P", None),
)


def get_builder(sphinx_args: List[str]):
    """Prepare the function that calls sphinx."""
    sphinx_command = [sys.executable, "-m", "sphinx"] + sphinx_args

    def build():
        """Generate the documentation using ``sphinx``."""

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


def check_env_pickle_exist(src: Path, dst: Path, reverse: bool = False) -> bool:
    pass


def folder_transfer(src: Path, dst: Path, reverse: bool = False) -> None:
    # check_env_pickle_exist()

    try:
        show(context="✅Done")
    except Exception as e:
        show(context=f"❌Error - Reason: {e}", error=True)

