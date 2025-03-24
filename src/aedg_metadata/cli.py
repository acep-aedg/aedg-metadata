"""Entry point for metadata generating CLI"""
from __future__ import annotations

from enum import Enum
from typing import Annotated

import typer

from .gen_meta import run_generate

app = typer.Typer()


class ExtentTypes(str, Enum):
    """Different ways to make spatial and temporal extents.
    Annotations failed syntax checks, or they would look like:
    infer: Annotated[str, "Infer the extent from the file qualities."] = "infer"
    calc: Annotated[str, "Calculate the extent from values in the file."] = "calc"
    specify: Annotated[str, "Read the extent from values in the config file."] = "specify"
    none: Annotated[str, "Do not include extent."] = "none"
    """
    infer = 'infer'
    calc = 'calc'
    specify = 'specify'
    none = 'none'


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
    bbox: Annotated[
        ExtentTypes,
        typer.Option(
            "--bbox", "-b",
            help="How the spatial bounding box should be determined."
        ),
    ] = ExtentTypes.specify,
    temporal: Annotated[
        ExtentTypes,
        typer.Option(
            "--time", "-t",
            help="How the temporal description should be determined."
        ),
    ] = ExtentTypes.specify,
    save: Annotated[
        bool,
        typer.Option(
            help="Write generated metadata to the file or else to the screen."
        ),
    ] = False,
) -> None:
    """To call gen_meta.py."""
    print(f"Hello {config} in {subdirectory}!")  # noqa: T201
    run_generate(config, subdirectory, bbox, temporal, save)
