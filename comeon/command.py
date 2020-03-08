from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import click

from ._typing import Callback
from ._typing import Color


class Command(click.Command):
    def __init__(
        self,
        name: str,
        context_settings: Optional[Dict[str, Any]] = None,
        callback: Optional[Callback] = None,
        params: Optional[List[click.Parameter]] = None,
        help: Optional[str] = None,
        epilog: Optional[str] = None,
        short_help: Optional[str] = None,
        options_metavar: str = "[OPTIONS]",
        add_help_option: bool = True,
        hidden: bool = False,
        deprecated: bool = False,
        arguments_color: Color = "white",
        arguments_help_color: Color = "white",
        options_color: Color = "white",
        options_help_color: Color = "white",
        command_color: Color = "white",
        command_help_color: Color = "white",
    ):
        """
        :param name: the name of the command to use unless a group overrides it.
        :param context_settings: an optional dictionary with defaults that are
                                 passed to the context object.
        :param callback: the callback to invoke.  This is optional.
        :param params: the parameters to register with this command.  This can
                       be either :class:`Option` or :class:`Argument` objects.
        :param help: the help string to use for this command.
        :param epilog: like the help string but it's printed at the end of the
                       help page after everything else.
        :param short_help: the short help to use for this command.  This is
                           shown on the command listing of the parent command.
        :param add_help_option: by default each command registers a ``--help``
                                option.  This can be disabled by this parameter.
        :param no_args_is_help: this controls what happens if no arguments are
                                provided.  This option is disabled by default.
                                If enabled this will add ``--help`` as argument
                                if no arguments are passed
        :param hidden: hide this command from help outputs.
        :param deprecated: issues a message indicating that
                           the command is deprecated.
        :param arguments_color: argument name display color
        :param arguments_help_color: argument help display color
        :param options_color: option name display color
        :param options_help_color: option help display color
        :param command_color: command name display color
        :param command_help_color: command help display color
        """
        super().__init__(
            name=name,
            context_settings=context_settings,
            callback=callback,
            params=params,
            help=help,
            epilog=epilog,
            short_help=short_help,
            options_metavar=options_metavar,
            add_help_option=add_help_option,
            hidden=hidden,
            deprecated=deprecated,
        )
        self.arguments_color = arguments_color
        self.arguments_help_color = arguments_help_color
        self.options_color = options_color
        self.options_help_color = options_help_color
        self.command_color = command_color
        self.command_help_color = command_help_color

    def format_options(
        self, ctx: click.Context, formatter: click.formatting.HelpFormatter
    ) -> None:
        """Writes all the options into the formatter if they exist."""
        opts = []
        for param in self.get_params(ctx):
            help_record = param.get_help_record(ctx)
            if help_record is None:
                continue
            rv, help = help_record
            rv = click.style(rv, fg=self.options_color)
            help = click.style(help, fg=self.options_help_color)
            if rv is not None:
                opts.append((rv, help))

        if opts:
            with formatter.section("Options"):
                formatter.write_dl(opts)
