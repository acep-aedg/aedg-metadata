"""To grab the header lines from all the CSV files and parse to get fieldnames"
This code is mostly from GitHub copilot 3/26/2025
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def find_geojson_files(directory: Path) -> list[Path]:
    """Find all the GeoJSON files in a Path."""
    return list(Path(directory).rglob('*.geojson'))


def read_attribute_names(file_path: Path) -> list[str]:
    """Collect a list of unique attribute names in a GeoJSON file."""

    names: list[str] = []
    with file_path.open() as file:
        data = json.load(file)
        if data['type'] == 'FeatureCollection':
            for feature in data['features']:
                #print(f'Attribute names in {file_path}: {list(feature["properties"].keys())}')
                names = names + list(feature["properties"].keys())
        elif data['type'] == 'Feature':
            #print(f'Attribute names in {file_path}: {list(data["properties"].keys())}')
            names = names + list(data["properties"].keys())
        else:
            print(f'Unknown GeoJSON type in {file_path}') # noqa: T201
    return list(set(names))


def main(directory: Path) -> None:
    """Accumulate all the attributes in a directory tree and parse for unique fieldnames."""

    # set-up
    fields: list[str] = []
    geojson_files = find_geojson_files(directory)

    for geojson_file in geojson_files:
        attributes = read_attribute_names(geojson_file)
        print(f'Attributes in {geojson_file.name} are: {attributes}')  # noqa: T201
        fields = fields + attributes

    # output
    fields = list(set(fields))
    fields.sort()
    for f in fields:
        print(f)  # noqa: T201


if __name__ == "__main__":
    
    # Check if a directory path was provided as an argument
    if len(sys.argv) > 1:
        # sys.argv[0] is the script name; sys.argv[1] is the first argument
        directory_path_str = sys.argv[1]
        directory = Path(directory_path_str)
    else:
        # Use the hardcoded path as a default if no argument is provided
        print(f"Error: Please provide a data directory")
        sys.exit(1)
        
    
    print(f"Processing: {directory}")
    
    if not directory.is_dir():
        print(f"Error: Directory not found at {directory}")
        sys.exit(1)

    main(directory)
