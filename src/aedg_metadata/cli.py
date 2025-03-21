"""Entry point for metadata generating CLI"""
from __future__ import annotations

from typing import Annotated

import typer

from .gen_meta import run_generate

app = typer.Typer()


@app.command()  # type: ignore[misc]
def greet(
    name: Annotated[str, typer.Argument(help="Last name of person to greet.")],
    count: Annotated[int, typer.Option(help="Number of times to repeat.")] = 1,
) -> None:
    """Simple program that greets NAME for a total of COUNT times."""
    for _x in range(count):
        print(f"Hello {name}!")  # noqa: T201


@app.command()  # type: ignore[misc]
def generate(
    config: Annotated[
        str,
        typer.Argument(
            help="File stem of config file (req)."
        ),
    ],
    subdirectory: Annotated[
        str,
        typer.Option(
            "--directory", "-d",
            help="Subdirectory of data/ where target file lives in the AEDG pond."
        ),
    ] = "public",
    save: Annotated[
        bool,
        typer.Option(
            help="Write generated metadata to the file or else to the screen."
        ),
    ] = False
) -> None:
    """To call gen_meta.py."""
    print(f"Hello {config} in {subdirectory}!")  # noqa: T201
    run_generate(config, subdirectory, save)
