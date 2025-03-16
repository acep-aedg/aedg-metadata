"""Entry point for metadata generating CLI"""
from __future__ import annotations

from typing import Annotated

import typer

app = typer.Typer()


@app.command()  # type: ignore[misc]
def hello(
    name: Annotated[str, typer.Argument(help="Last name of person to greet.")],
    count: Annotated[int, typer.Option(help="Number of times to repeat.")] = 1,
) -> None:
    """Simple program that greets NAME for a total of COUNT times."""
    for _x in range(count):
        print(f"Hello {name}!")  # noqa: T201


if __name__ == "__main__":
    app()
