from typing import Any
from typing import Callable
from typing import Iterable
from typing import Type

import click

from typing_extensions import Literal


Callback = Callable[[Type[click.Context], Type[click.Parameter], Any], None]

Color = Literal[
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
    "bright_black",
    "bright_red",
    "bright_yellow",
    "bright_blue",
]

Autocompletion = Callable[[Type[click.Context], Iterable[str], str], None]
