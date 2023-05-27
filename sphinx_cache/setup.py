import os
import shutil
from pathlib import Path
from typing import Any, Dict

from sphinx.application import Sphinx

from sphinx_cache.logging import show
from sphinx_cache.utils import check_env_pickle_exist
from sphinx_cache.version import __version__


def setup(app: Sphinx) -> Dict[str, Any]:
    # Define config values
    app.add_config_value("cache_store_path", ".cache/", "html", types=[str])
    app.add_config_value("cache_doctree_path", "_build/.doctrees", "html", types=[str])

    # Make connections to events
    app.connect("builder-inited", build_init)
    app.connect("build-finished", write_cache)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }


# ----- SPHINX-EVENTS FUNCTIONS ----- #
def build_init(app: Sphinx) -> None:
    """
    Function to set the cache_doctree_path as directory for storing pickled doctrees and
    also call the :meth:`restore_cache()` function to restore cache

    :param app: Sphinx application
    :return:
    """
    app.doctreedir = os.path.realpath(Path(app.confdir).joinpath(app.config.cache_doctree_path))
    # Call restore_cache function to restore cache
    restore_cache(app)


def restore_cache(app: Sphinx) -> None:
    """
    Function to restore contents from the **cache** directory to the **.doctrees** directory

    :param app: Sphinx application
    :return:
    """
    doctree_dir = Path(app.doctreedir)
    cache_dir = Path(app.confdir).joinpath(app.config.cache_store_path)
    show(context="- Restoring cache...")

    env_pickle_exist = check_env_pickle_exist(doctree_dir)
    # Restore cache only if no `environment.pickle` exists in .doctrees directory
    if not env_pickle_exist:
        if not cache_dir.exists():
            show(context=f"- Creating cache directory: {app.config.cache_store_path}")
            cache_dir.mkdir(parents=True)

        if cache_dir.joinpath("environment.pickle") not in cache_dir.iterdir():
            show(
                context=f"- ⚠️ Skipped cache restore"
                f" - Reason: `environment.pickle` file not found in {app.config.cache_store_path}"
            )
        else:
            try:
                show(
                    context=f"- Restoring `.doctrees` contents from {app.config.cache_store_path} "
                    f"to {app.config.cache_doctree_path}"
                )
                shutil.copytree(
                    cache_dir, doctree_dir, dirs_exist_ok=True
                )  # Copy cache directory to .doctrees directory
                show(context="- ✅ Restoring Done")
            except Exception as e:
                show(context=f"- ❌ Error - Reason: {e}", error=True)
    else:
        show(
            context=f"- ⚠️ Skipped cache restore"
            f" - Reason: `environment.pickle` file exists already in {app.config.cache_doctree_path}"
        )


def write_cache(app: Sphinx, exception: Exception) -> None:
    """
    Function to store contents from the **.doctrees** directory to the **cache** directory.

    :param app: Sphinx application
    :param exception: Exception if Sphinx build was not successful
    :return:
    """
    doctree_dir = Path(app.doctreedir)
    cache_dir = Path(app.confdir).joinpath(app.config.cache_store_path)

    # Store cache only if no error occurred during Sphinx build
    if not exception:
        show(context="- Storing cache...")

        if not cache_dir.exists():
            show(context=f"- Creating cache directory: {app.config.cache_store_path}")
            cache_dir.mkdir(parents=True)

        env_pickle_exist = check_env_pickle_exist(doctree_dir)
        if env_pickle_exist:
            try:
                shutil.rmtree(cache_dir, ignore_errors=True)  # Delete old cache directory
                show(
                    context=f"- Storing `.doctrees` contents from {app.config.cache_doctree_path} "
                    f"to {app.config.cache_store_path}"
                )
                shutil.copytree(
                    doctree_dir, cache_dir, dirs_exist_ok=True
                )  # Copy .doctrees directory to cache directory
                show(context="- ✅ Storing Done")
            except Exception as e:
                show(context=f"- ❌ Error - Reason: {e}", error=True)
        else:
            show(
                context=f"️- ⚠️ Skipped cache store"
                f" - Reason: `environment.pickle` file does not exist in {app.config.cache_doctree_path}"
            )
