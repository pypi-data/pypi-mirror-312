import logging

import typer

from genov.welcome.welcomeTyper import allo

_logger: logging.Logger = logging.getLogger(__name__)

app = typer.Typer()

# noinspection PyTypeChecker
app.add_typer(allo)

if __name__ == '__main__':
    app()