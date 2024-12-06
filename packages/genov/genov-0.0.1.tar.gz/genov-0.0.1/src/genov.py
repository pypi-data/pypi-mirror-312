import logging
from inspect import stack
from typing import Annotated

import typer
import rich
from genov.welcome import welcomeTyper

_logger: logging.Logger = logging.getLogger(__name__)

app = typer.Typer(
    chain=True,             # To chain commands
    no_args_is_help=True    # when no parameter, help is displayed
)

app.command("welcome")(welcomeTyper.welcomeTyper)

@app.callback()
def main(
        ctx_context: typer.Context,
        b_verbose: Annotated[
            bool,
            typer.Option(
                "--verbose/--no-verbose",
                "-v",
                help="Level of logging verbosity: INFO (--verbose), WARNING (default) or ERROR (--no-verbose).",
                show_default="WARNING"
            )
        ] = None
):
    """
    Genov tool box, the application with all the commands you need in your day-to-day work at Genovation.

    Use the VERBOSE parameter to set the level of logs you need, and let you guide by the HELP.
    """
    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")
    _str_log_msg: str

    if b_verbose is True:
        _str_log_msg = f"[bold red]Logging: INFO[/bold red]"
        logging.basicConfig(level="INFO")
    elif b_verbose is False:
        _str_log_msg = f"[bold blue]Logging: ERROR[/bold blue]"
        logging.basicConfig(level="ERROR")
    else:
        _str_log_msg = f"[bold orange]Logging: WARNING[/bold orange]"
        logging.basicConfig(level="WARNING")

    rich.print(
        rich.panel.Panel(
            f"{_str_log_msg}\n"
            f"Welcome to the Genovation toolbox!")
    )

    # Ensure that ctx_context.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    # This is effectively the context, that is shared across commands
    if ctx_context.obj:
        pass
    else:
        _logger.debug(f"We call function ctx_context.ensure_object(dict)")
        ctx_context.ensure_object(dict)

    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")

if __name__ == '__main__':
    app()