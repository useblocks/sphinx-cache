import os
from pathlib import Path

import click

from .logging import show
from .utils import get_builder, restore_command_invoked, store_command_invoked
from .version import __version__

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__, prog_name="Sphinx-Cache", message="%(prog)s, version %(version)s")
def cli() -> None:
    pass


@cli.command("store", short_help="command to store contents from `.doctrees` folder to target folder")
@click.argument(
    "doctreedir",
    type=click.Path(exists=True, file_okay=False),
    default="docs/_build/html/.doctrees",
)
@click.argument(
    "cachedir",
    type=click.Path(file_okay=False),
    default="docs/_build/cache",
)
def sc_store(doctreedir: str, cachedir: str) -> None:
    """
    Command to store contents from the `.doctrees` directory to the cache directory.

    Args: \n
    \tDOCTREEDIR is the path to the `.doctrees` directory [default: "docs/_build/html/.doctrees"].\n
    \tCACHEDIR is the path to the cache directory [default: "docs/_build/cache"].
    """
    show(command="> Invoke `sphinx-cache store` command")

    if not Path(os.path.realpath(cachedir)).exists():
        show(context=f"- Creating new cache directory: {cachedir}...")
        Path(os.path.realpath(cachedir)).mkdir(parents=True)

    store_command_invoked(doctreedir, cachedir)


@cli.command("restore", short_help="command to restore contents from target folder to `.doctrees` folder")
@click.argument(
    "cachedir",
    type=click.Path(exists=True, file_okay=False),
    default="docs/_build/cache",
)
@click.argument(
    "doctreedir",
    type=click.Path(file_okay=False),
    default="docs/_build/html/.doctrees",
)
def sc_restore(cachedir: str, doctreedir: str) -> None:
    """
    Command to restore contents from the cache directory to the `.doctrees` directory.

    Args: \n
    \tCACHEDIR is the path to the cache directory [default: "docs/_build/cache"].\n
    \tDOCTREEDIR is the path to the `.doctrees` directory [default: "docs/_build/html/.doctrees"].
    """
    show(command="> Invoke `sphinx-cache restore` command")

    if not Path(os.path.realpath(doctreedir)).exists():
        show(context=f"- Creating `.doctrees` directory: {doctreedir}...")
        Path(os.path.realpath(doctreedir)).mkdir(parents=True)

    restore_command_invoked(doctreedir, cachedir)


@cli.command(
    "build",
    short_help="command to build Sphinx docs and also execute the `store` and `restore` commands",
    context_settings={"ignore_unknown_options": True, "allow_extra_args": True},
)
@click.option(
    "--cachedir",
    required=True,
    type=click.Path(file_okay=False),
    metavar="<Path>",
    default="docs/_build/cache",
    show_default=True,
    help="path to the directory for caching",
)
@click.pass_context
def sc_build(ctx: click.core.Context, cachedir: str) -> None:
    """
    Command to build Sphinx docs and also execute the `store` and `restore` commands.

    Sphinx's build options: The `sphinx_cache build` command forwards all `sphinx-build`
    options passed, as it is to Sphinx. Please look at `sphinx-build --help` for more information. \f

    Args: \n
        \tSOURCEDIR is path to documentation source directory. \n
        \tOUTPUTDIR is path to documentation output directory.

    So the internal workflow is restore -> build -> store
    """
    show(command="> Running `sphinx-cache build` command.")

    # Default args for sphinx build if user doesn't provide them
    if not ctx.args:
        ctx.args.extend(["-j", "auto", "docs", "docs/_build/html"])

    sourcedir = ctx.args[-2]
    outputdir = ctx.args[-1]

    cache_dir = Path(os.path.realpath(cachedir))  # path to cache dir
    doctreedir = outputdir + "/.doctrees"  # path to .doctree dir

    if not cache_dir.exists():
        show(context=f"- Creating new cache directory: {cachedir}...")
        cache_dir.mkdir(parents=True)

    # Invoke the restore command
    ctx.invoke(sc_restore, cachedir=cachedir, doctreedir=doctreedir)

    # Invoke Sphinx Build command
    show(context=f"- Building Sphinx docs from {sourcedir} to {outputdir}")
    sphinx_build_args = ctx.args  # get only the user-specified Sphinx build arguments
    sphinx_builder = get_builder(sphinx_build_args)  # build sphinx docs
    show(context="- ✅ Sphinx build was successful.") if sphinx_builder == 0 else show(
        context="- ❌ Sphinx build was unsuccessful."
    )

    # Invoke the store command
    ctx.invoke(sc_store, doctreedir=doctreedir, cachedir=cachedir)

    show(context="- ✅ Build command completed successfully (^-^)")
