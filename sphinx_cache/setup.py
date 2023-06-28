import os
import shutil
from pathlib import Path
from typing import Any, Dict

from sphinx.application import Sphinx
from sphinx.config import Config

from sphinx_cache.logging import show
from sphinx_cache.utils import check_env_pickle_exist
from sphinx_cache.version import __version__


def setup(app: Sphinx) -> Dict[str, Any]:
    # Define config values
    app.add_config_value("cache_store_path", ".cache/", "html", types=[str])
    app.add_config_value("cache_doctree_path", "_build/.doctrees", "html", types=[str])

    # Make connections to events
    app.connect("config-inited", config_init)
    app.connect("builder-inited", build_init)
    app.connect("build-finished", write_cache)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }


# ----- SPHINX-EVENTS FUNCTIONS ----- #
def config_init(app: Sphinx, config: Config):
    """
    Function to configure the cache_doctree_path as directory for storing pickled doctrees.

    :param app: Sphinx application
    :param config: Sphinx configuration
    :return:
    """
    doctree_dir = Path(app.confdir).joinpath(config.cache_doctree_path)
    app.doctreedir = os.path.realpath(doctree_dir)
    # Create doctrees directory
    if not doctree_dir.exists():
        doctree_dir.mkdir(parents=True)


def build_init(app: Sphinx) -> None:
    """
    Function to call the :meth:`restore_cache()` function to restore cache

    :param app: Sphinx application
    :return:
    """
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
    if env_pickle_exist:
        show(context="- ⚠️ Skipped cache restore because we can use the found cache.")
    else:
        if not cache_dir.exists():
            show(context=f"- Creating cache directory: {app.config.cache_store_path}")
            cache_dir.mkdir(parents=True)

        if not cache_dir.joinpath("environment.pickle").exists():
            show(context="- ⚠️ Skipped cache restore because we cannot find any cache to restore.")
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
    if exception:
        show(context="️- ⚠️ Skipped cache store because Sphinx build encountered some errors.")
    else:
        show(context="- Storing cache...")

        if not cache_dir.exists():
            show(context=f"- Creating cache directory: {app.config.cache_store_path}")
            cache_dir.mkdir(parents=True)

        env_pickle_exist = check_env_pickle_exist(doctree_dir)
        # Store cache only if `environment.pickle` exists in .doctrees directory
        if not env_pickle_exist:
            show(context="️- ⚠️ Skipped cache store because we can not find any cache to store.")
        else:
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
