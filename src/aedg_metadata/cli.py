"""Entry point for metadata generating CLI"""
from __future__ import annotations

import json
from pprint import pprint
from typing import Annotated

import typer

from aedg_metadata import ExtentTypes

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

    package = run_generate(config, subdirectory, bbox, temporal)

    if save:
        with package.output_file.open(mode="w") as file:
            json.dump(package.data_package, file, indent=4)
            # for pre-commit end of file check
            file.write("\n")
    else:
        # write output to the screen for debugging
        pprint(package.data_package, depth=None, sort_dicts=False)  # noqa: T203
