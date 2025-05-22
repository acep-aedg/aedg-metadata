"""Functions to help things along."""
from __future__ import annotations

import urllib
import urllib.request
from typing import Any

from jsonschema import ValidationError, validate
from oemetadata.latest.schema import OEMETADATA_LATEST_SCHEMA


def check_schema(package: dict[Any, Any]) -> None:
    """Function from OEMetadata to check schema against standard"""
    try:
        validate(package, OEMETADATA_LATEST_SCHEMA)
        print("Metadata is valid according to OEMetadata Schema (Latest).")  # noqa: T201
    except ValidationError as e:
        print(  # noqa: T201
            "Cannot validate the metadata according to OEMetadata Schema (Latest)!", e
        )


def check_fields(package: dict[Any, Any]) -> None:
    """Function to check that all the columns in the file are described."""

    columns = parse_csv_header(package)
    fields = []
    for field in package['resources'][0]['schema']['fields']:
        fields.append(field['name'])

    try:
        assert set(fields) == set(columns)
        print("All columns names are described.")  # noqa: T201
    except AssertionError as e:
        msg = f"Columns {set(columns) - set(fields)} are not in metadata."
        raise KeyError(msg) from e


def parse_csv_header(package: dict[Any, Any]) -> Any:
    """Get the header line from the URL of a CSV documented in a data package.
       Bonus: checks that URL is valid too."""

    url = package['resources'][0]['path']
    try:
        with urllib.request.urlopen(url) as response:
            header = next(response)
    except urllib.error.HTTPError as e:
        msg = f'Metadata references non-existent file {url}'
        raise ValueError(msg) from e
    return header.decode().strip().split(',')
