"""Functions to inspect local files and validate metadata schemas locally."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Set, Union  # noqa: UP035

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


def check_fields(package: dict[Any, Any], local_path: Union[str, Path, None] = None) -> None:
    """Checks that all columns/properties in the local file are described in the metadata."""
    columns = parse_combined_header(package, local_path)
    fields = [field['name'] for field in package['resources'][0]['schema']['fields']]

    try:
        assert set(fields) == set(columns)
        print("All columns names are described.")  # noqa: T201
    except AssertionError as e:
        msg = f"Columns {set(columns) - set(fields)} are not in metadata."
        raise KeyError(msg) from e


def _parse_csv_header_logic(file_path: Union[str, Path]) -> List[str]:
    """Reads the first line of a local CSV file and returns the column names."""
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"Local CSV file does not exist: {path.resolve()}")

    with open(path, 'r', encoding='utf-8') as f:
        header_line = next(f).strip()

    return header_line.split(',')


def _parse_geojson_header_logic(file_path: Union[str, Path]) -> List[str]:
    """Reads a local GeoJSON file and returns attribute property names."""
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"Local GeoJSON file does not exist: {path.resolve()}")

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    attribute_names: Set[str] = set()

    if data.get("type") == "FeatureCollection" and isinstance(data.get("features"), list):
        # Sample only the first 10 features for speed
        for feature in data["features"][:10]:
            properties = feature.get("properties")
            if isinstance(properties, dict):
                attribute_names.update(properties.keys())

    elif data.get("type") == "Feature" and isinstance(data.get("properties"), dict):
        attribute_names.update(data["properties"].keys())

    elif "type" not in data:
        raise ValueError(f'GeoJSON file at {path} is missing the mandatory "type" field.')

    return sorted(list(attribute_names))


def parse_combined_header(package: Dict[Any, Any], local_path: Union[str, Path, None] = None) -> List[str]:
    """
    Reads field names directly from a local CSV or GeoJSON file.
    If local_path is not explicitly passed, resolves the filename from the package metadata.
    """
    if local_path:
        target_path = Path(local_path)
    else:
        try:
            raw_path = package['resources'][0]['path']
            # Take only the filename to prevent web URLs from interfering
            filename = Path(raw_path).name
            target_path = Path("../aedg-data-pond/pub") / filename
        except (KeyError, IndexError) as e:
            raise ValueError(f"Package structure error: missing expected resource path key: {e}") from e

    ext = target_path.suffix.lower()

    if ext == '.csv':
        return _parse_csv_header_logic(target_path)
    elif ext == '.geojson':
        return _parse_geojson_header_logic(target_path)
    else:
        raise ValueError(f"Unsupported local file extension: '{ext}'. Must be .csv or .geojson.")
