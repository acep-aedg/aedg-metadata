"""Functions to help things along."""
from __future__ import annotations

import urllib
from typing import Any

import pandas as pd
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
    """Function to check that all the columns in the file are described.
    Bonus: checks that path exists too."""

    path = package['resources'][0]['path']
    try:
        columns = pd.read_csv(path, header=0, nrows=0).columns.tolist()
    except urllib.error.HTTPError as e:  # type: ignore[attr-defined]
        msg = f'Metadata references non-existent file {path}'
        raise ValueError(msg) from e

    fields = []
    for field in package['resources'][0]['schema']['fields']:
        fields.append(field['name'])

    try:
        assert set(fields) == set(columns)
        print("All columns names are described.")  # noqa: T201
    except AssertionError as e:
        msg = f"Columns {set(columns) - set(fields)} are not in metadata."
        raise KeyError(msg) from e
