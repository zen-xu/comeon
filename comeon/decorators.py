import inspect

from typing import Any
from typing import Callable
from typing import Optional
from typing import Type

import click

from click.decorators import _make_command  # type: ignore
from typing_extensions import Literal

from .command import Command
from .params import Argument
from .params import Option
from .params import Param
from .utils import get_typed_signature


try:
    from collections.abc import Iterable as IterableCls
except ImportError:
    from collections import Iterable as IterableCls


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
        f = _inject_params(f)
        cmd = _make_command(f, name, attrs, cls)
        cmd.__doc__ = f.__doc__
        return cmd

    return decorator


def _inject_params(f: Callable[..., None]) -> Callable[..., None]:
    signature = get_typed_signature(f)
    for _, param in reversed(list(signature.parameters.items())):
        f = _inject_param(f, param)
    return f


def _param_memo(f: Callable[..., None], param: click.Parameter) -> None:
    if not hasattr(f, "__click_params__"):
        f.__click_params__ = []  # type: ignore
    f.__click_params__.append(param)  # type: ignore


def _inject_param(
    f: Callable[..., None], param: inspect.Parameter
) -> Callable[..., None]:
    assert param.annotation != param.empty, f"Param {param.name} must add annotation"

    default = param.default
    param_maker: Param
    if isinstance(default, Param):
        param_maker = default
    else:
        if param.annotation == bool:
            param_name = param.name.replace("_", "-")
            default = False if param.default == param.empty else param.default
            param_maker = Option(
                *[f"--{param_name}"],
                default=default,
                show_default=True,
                is_flag=True,
                type=bool,
            )
        elif (
            param.kind == inspect._ParameterKind.POSITIONAL_ONLY  # type: ignore
        ):
            param_maker = Argument(param_decl=param.name, required=True)
        elif (
            param.kind == inspect._ParameterKind.POSITIONAL_OR_KEYWORD  # type: ignore
        ):
            if param.default == param.empty:
                param_maker = Argument(param_decl=param.name, required=False)
            else:
                param_name = param.name.replace("_", "-")
                param_maker = Option(
                    *[f"--{param_name}"],
                    default=param.default,
                    show_default=True,
                    required=False,
                )
        elif (
            param.kind == inspect._ParameterKind.KEYWORD_ONLY  # type: ignore
        ):
            param_name = param.name.replace("_", "-")
            if param.default == param.empty:
                param_default = None
            else:
                param_default = param.default
            param_maker = Option(
                *[f"--{param_name}"],
                default=param_default,
                show_default=default is not None,
                required=(param.default == param.empty),
            )
        elif (
            param.kind == inspect._ParameterKind.VAR_POSITIONAL  # type: ignore
        ):
            param_name = param.name.replace("_", "-")
            param_maker = Option(*[f"--{param_name}"], multiple=True, required=False)
        else:
            raise ValueError(f"Unsupported Parameterkind: {param.kind} => {param.name}")

    if not param_maker.args["param_decls"]:
        param_name = param.name
        if isinstance(param_maker, Option):
            param_name = param_name.replace("_", "-")
            param_maker.update(param_decls=[f"--{param_name}"])
        else:
            param_maker.update(param_decls=[param_name])

    try:
        origin_type = param.annotation.__origin__
    except AttributeError:
        origin_type = param.annotation

    has_subclasses = getattr(origin_type, "__subclasses__", None) is not None
    iter_types = [list, set, tuple, IterableCls]
    if (origin_type in iter_types) or (
        has_subclasses
        and (
            issubclass(origin_type, IterableCls)
            and not issubclass(param.annotation, str)
        )
    ):
        if isinstance(param_maker, Option):
            param_maker.update(multiple=True)
        else:
            param_maker.update(nargs=-1)

    try:
        if param.annotation.__origin__ == Literal:
            choices = param.annotation.__args__
        elif param.annotation.__args__[0].__origin__ == Literal:
            choices = param.annotation.__args__[0].__args__
        param_maker.update(type=click.Choice(choices))
    except AttributeError:
        pass

    # update type
    if origin_type in [int, float, str, bool]:
        param_maker.update(type=origin_type)

    click_param = param_maker.make_click_param()

    # click param name use function arg param name
    click_param.name = param.name

    _param_memo(f, click_param)

    return f
