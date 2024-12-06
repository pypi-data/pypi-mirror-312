import logging
import typer
from rich import print
from rich.panel import Panel
from rich.tree import Tree
from rich.console import Console

from genov.welcome.welcome import welcome

_logger: logging.Logger = logging.getLogger(__name__)

app = typer.Typer()

@app.command()
def welcomeTyper(name: str):
    """
    Welcome to the Genovation toolbox!
    This command will greet NAME, and return welcome message.
    """

    typer.secho(
        "welcome",
        blink=True,
        bold=True
    )

    print(
        Panel(
            f"[bold red]Welcome![/bold red]\n"
            f"[green]{welcome(name=name)}[/green]\n"
            f"shooting! :boom:"
        )
    )

    console = Console()

    tree = Tree("root")
    tree.add("JSG")
    tree.add("YDA")
    print(
        f"why? {tree}"
    )

    err_console = Console(stderr=True)
    err_console.print("Here is something written to standard error")

