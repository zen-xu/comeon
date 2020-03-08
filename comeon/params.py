from typing import Any
from typing import Dict
from typing import Iterable
from typing import Optional
from typing import Type

import click

from ._typing import Autocompletion
from ._typing import Callback


class Param(object):
    param_class: Type[click.Parameter]

    def __init__(self, **args: Any) -> None:
        self.args: Dict[str, Any] = args

    def make_click_param(self) -> click.Parameter:
        return self.param_class(**self.args)

    def update(self, **update_params: Any) -> None:
        self.args.update(**update_params)


class Argument(Param):
    param_class = click.Argument

    def __init__(
        self,
        param_decl: Optional[str] = None,
        *,
        default: Optional[Any] = None,
        type: Optional[str] = None,
        required: bool = False,
        callback: Optional[Callback] = None,
        nargs: Optional[int] = None,
        metavar: Optional[str] = None,
        expose_value: bool = True,
        is_eager: bool = False,
        envvar: Optional[str] = None,
        autocompletion: Optional[Autocompletion] = None,
    ):
        if param_decl:
            param_decls = [param_decl]
        else:
            param_decls = []
        super().__init__(
            param_decls=param_decls,
            default=default,
            type=type,
            required=required,
            callback=callback,
            nargs=nargs,
            metavar=metavar,
            expose_value=expose_value,
            is_eager=is_eager,
            envvar=envvar,
            autocompletion=autocompletion,
        )


class Option(Param):
    param_class = click.Option

    def __init__(
        self,
        *param_decls: Iterable[str],
        default: Optional[Any] = None,
        show_default: bool = False,
        prompt: bool = False,
        confirmation_prompt: bool = False,
        hide_input: bool = True,
        is_flag: Optional[bool] = None,
        flag_value: Optional[Any] = None,
        multiple: bool = False,
        count: bool = False,
        allow_from_autoenv: bool = False,
        type: Optional[Any] = None,
        help: Optional[str] = None,
        hidden: bool = False,
        show_choices: bool = True,
        show_envvar: bool = False,
        autocompletion: Optional[Autocompletion] = None,
    ):
        super().__init__(
            param_decls=param_decls,
            default=default,
            show_default=show_default,
            prompt=prompt,
            confirmation_prompt=confirmation_prompt,
            hide_input=hide_input,
            is_flag=is_flag,
            flag_value=flag_value,
            multiple=multiple,
            count=count,
            allow_from_autoenv=allow_from_autoenv,
            type=type,
            help=help,
            hidden=hidden,
            show_choices=show_choices,
            show_envvar=show_envvar,
            autocompletion=autocompletion,
        )
