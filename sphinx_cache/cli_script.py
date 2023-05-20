import os
from typing import Tuple

import click
from pathlib import Path
from click_option_group import optgroup


from .logging import show
from .utils import folder_transfer
from .version import __version__

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__, prog_name="Sphinx-Cache", message="%(prog)s, version %(version)s")
def cli() -> None:
    pass


@cli.command("store", short_help="command to store contents from `.doctrees` folder to target folder")
@click.argument('sourcedir', type=click.Path(exists=True, file_okay=False))
@click.argument('targetdir', type=click.Path(file_okay=False))
def sc_store(sourcedir: str, targetdir: str) -> None:
    """
    Command to copy contents of the `.doctrees` folder to a target folder.

    Args: \n
    \tSOURCEDIR is path to source folder. \n
    \tTARGETDIR is path to destination folder.
    """
    src_dir = Path(os.path.realpath(sourcedir))
    out_dir = Path(os.path.realpath(targetdir))

    if not os.path.exists(out_dir):
        show(context=f"Creating target folder: {targetdir}")
        os.makedirs(out_dir)

    show(context=f"Storing `.doctrees` cache from {sourcedir} to {targetdir}")
    folder_transfer(src_dir, out_dir)


@cli.command("restore", short_help="command to restore contents from target folder to `.doctrees` folder")
@click.argument('sourcedir', type=click.Path(exists=True, file_okay=False))
@click.argument('targetdir', type=click.Path(exists=True, file_okay=False))
def sc_restore(sourcedir: str, targetdir: str) -> None:
    """
    Command to restore contents of the target folder to the `.doctrees` folder.

    Args: \n
    \tSOURCEDIR is path to source folder. \n
    \tTARGETDIR is path to destination folder.
    """
    src_dir = Path(os.path.realpath(sourcedir))
    out_dir = Path(os.path.realpath(targetdir))

    show(context=f"Restoring `.doctrees` cache from {sourcedir} to {targetdir}")
    folder_transfer(src_dir, out_dir, reverse=True)


@cli.command("build", short_help="command to build Sphinx docs and also execute the `store` and `restore` commands")
@click.argument('sourcedir', type=click.Path(exists=True, file_okay=False), metavar="<Path>")
@click.argument('outputdir', type=click.Path(file_okay=False), metavar="<Path>")
@click.option('--targetdir', required=True, type=click.Path(file_okay=False), metavar="<Path>", help="path to cache "
                                                                                                     "target directory")
@optgroup.group("Sphinx's build options",
                help="The following options are forwarded as-is to Sphinx. Please look at `sphinx-build --help` for "
                     "more information.")
@optgroup.option('-b', default='html', help='builder to use (default: html)', show_default=True, metavar="<BUILDER>")
@optgroup.option('-a', is_flag=True, help="write all files [default: only write new and changed files]")
@optgroup.option('-E', is_flag=True, help="don't use a saved environment, always read all files")
@optgroup.option('-d', type=click.Path(file_okay=False), help='path for the cached environment and doctree files [default: OUTPUTDIR/.doctrees]', metavar="<PATH>")
@optgroup.option('-j', '--jobs', default="1", metavar='N', help="build in parallel with N processes where possible (special value 'auto' will set N to cpu-count)")
@optgroup.option('-c', type=click.Path(file_okay=False), help='path where configuration file (conf.py) is located [default: same as SOURCEDIR]', metavar="<PATH>")
@optgroup.option('-D', 'D', multiple=True, default=[], metavar='setting=value', help="override a setting in configuration file")
@optgroup.option('-A', 'A', multiple=True, default=[], metavar='name=value', help="pass a value into HTML templates")
@optgroup.option('-t', multiple=True, default=[], metavar='TAG', help="define tag: include 'only' blocks with TAG")
@optgroup.option('-n', is_flag=True, help="nit-picky mode, warn about all missing references")
@optgroup.option('-v', count=True, default=0, help="increase verbosity (can be repeated)")
@optgroup.option('-q', is_flag=True, help="no output on stdout, just warnings on stderr")
@optgroup.option('-Q', 'Q', is_flag=True, help="no output on stdout, not even warnings")
@optgroup.option('--color/--no-color', ' /-N', default=False, help="emit or don't emit colored output [default: auto-detect]")
@optgroup.option('-w', type=click.Path(dir_okay=False), help='write warnings (and errors) to given file', metavar="<FILE>")
@optgroup.option('-W', 'W', is_flag=True, help="turn warnings into errors")
@optgroup.option('--keep-going', is_flag=True, help="turn warnings into errors")
@optgroup.option('-T', 'T', is_flag=True, help="show full traceback on exception")
@optgroup.option('-P', 'P', is_flag=True, help="run Pdb on exception")
def sc_build(**params):
    """
    Command to build Sphinx docs and also execute the `store` and `restore` commands.

    Args: \n
    \tSOURCEDIR is path to documentation source directory. \n
    \tOUTPUTDIR is path to documentation output directory.
    """
    pass
