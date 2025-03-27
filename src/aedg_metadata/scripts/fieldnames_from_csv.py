"""To grab the header lines from all the CSV files and parse to get fieldnames"
This code is mostly from GitHub copilot 3/26/2025
"""
from __future__ import annotations

import csv
from pathlib import Path


def find_csv_files(directory: Path) -> list[Path]:
    """Find all the CSV files in a Path."""
    return list(Path(directory).rglob('*.csv'))


def read_first_line(file_path: Path) -> list[str]:
    """Read the first line of a file."""
    with file_path.open(newline='') as csvfile:
        reader = csv.reader(csvfile)
        return next(reader)  # Read the first line


def main(directory: Path) -> None:
    """Accumulate all the header lines in a directory tree and parse for unique fieldnames."""

    # set-up
    fields: list[str] = []
    csv_files = find_csv_files(directory)

    # get those header lines
    for csv_file in csv_files:
        columns = read_first_line(csv_file)
        print(f'Column headers in {csv_file.name} are: {columns}')  # noqa: T201
        fields = fields + columns

    # output
    fields = list(set(fields))
    fields.sort()
    for f in fields:
        print(f)  # noqa: T201


if __name__ == "__main__":

    directory = Path(__file__).parents[4] / "aedg-data-pond" / "data"
    print(f"Processing: {directory}")  # noqa: T201

    main(directory)
