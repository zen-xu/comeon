from typing import Any
from typing import Callable
from typing import Optional
from typing import Type

import click

from click.decorators import _make_command  # type: ignore

# Circular dependencies between core and decorators
from .core import Command  # noqa


def command(
    name: Optional[str] = None, cls: Type[click.Command] = None, **attrs: Any
) -> Callable[[Callable[..., None]], Callable[..., None]]:
    r"""
    :param name: the name of the command.  This defaults to the function
                 name with underscores replaced by dashes.
    :param cls: the command class to instantiate.  This defaults to
                :class:`Command`.
    """
    if cls is None:
        cls = Command

    def decorator(f: Callable[..., None]) -> Callable[..., None]:
        cmd = _make_command(f, name, attrs, cls)
        cmd.__doc__ = f.__doc__
        return cmd

    return decorator
