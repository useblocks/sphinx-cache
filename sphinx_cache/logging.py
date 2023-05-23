import shlex
from typing import List, Optional, Tuple, Union

from colorama import Fore, Style


def _log(text: str, *, colour: str) -> None:
    print(f"{Fore.GREEN}[sphinx-cache] {colour}{text}{Style.RESET_ALL}")


def show(*, context: Optional[str] = None, command: Optional[Union[List, Tuple, str]] = None, error: bool = False):
    """Show context and command-to-be-executed, with nice formatting and colors."""
    if context is not None and not error:
        _log(context, colour=Fore.CYAN)
    if command is not None:
        if isinstance(command, (list, tuple)):
            _log("> " + " ".join(shlex.quote(s) for s in command), colour=Fore.MAGENTA)
        elif isinstance(command, str):
            _log(command, colour=Fore.MAGENTA)
    if context is not None and error:
        _log(context, colour=Fore.RED)
