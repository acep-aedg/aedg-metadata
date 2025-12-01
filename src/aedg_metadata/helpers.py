"""Functions to help things along."""
from __future__ import annotations

import json
import urllib
import urllib.error
import urllib.request
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


def check_fields(package: dict[Any, Any]) -> None:
    """Function to check that all the columns in the file are described."""

    columns = parse_combined_header(package)
    fields = []
    for field in package['resources'][0]['schema']['fields']:
        fields.append(field['name'])

    try:
        assert set(fields) == set(columns)
        print("All columns names are described.")  # noqa: T201
    except AssertionError as e:
        msg = f"Columns {set(columns) - set(fields)} are not in metadata."
        raise KeyError(msg) from e



def _parse_csv_header_logic(url: str) -> List[str]:
    """Reads the first line of a CSV from a URL and splits it into column names."""
    try:
        with urllib.request.urlopen(url) as response:
            header_line = next(response).decode().strip()
    except urllib.error.HTTPError as e:
        msg = f'Metadata references non-existent file {url}'
        raise ValueError(msg) from e
    return header_line.split(',')


def _parse_geojson_header_logic(url: str) -> List[str]:
    """Fetches GeoJSON, parses features, and returns unique attribute names."""
    data: Dict[str, Any] = {}
    attribute_names: Set[str] = set()
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)

    except (urllib.error.HTTPError, json.JSONDecodeError, Exception) as e:
        msg = f"Error processing GeoJSON file at {url}: {type(e).__name__}"
        raise ValueError(msg) from e

    if data.get("type") == "FeatureCollection" and isinstance(data.get("features"), list):
        # Sample only the first 10 features for speed
        for feature in data["features"][:10]:
            properties = feature.get("properties")
            if isinstance(properties, dict):
                attribute_names.update(properties.keys())
    
    elif data.get("type") == "Feature" and isinstance(data.get("properties"), dict):
        attribute_names.update(data["properties"].keys())

    elif "type" not in data:
        raise ValueError(f'GeoJSON file at {url} is missing the mandatory "type" field.')

    return sorted(list(attribute_names))


def parse_combined_header(package: Dict[Any, Any]) -> List[str]:
    """
    Parses the header/field names from a data package, handling both CSV and GeoJSON.
    """
    try:
        url: str = package['resources'][0]['path']
    except (KeyError, IndexError) as e:
        raise ValueError(f"Package structure error: missing expected resource path key: {e}") from e

    file_extension = Path(url.lower()).suffix
    
    if file_extension == '.csv':
        return _parse_csv_header_logic(url)
    
    elif file_extension == '.geojson':
        return _parse_geojson_header_logic(url)
        
    else:
        raise ValueError(f"Unsupported file type detected: {file_extension}. Must be .csv or .geojson.")