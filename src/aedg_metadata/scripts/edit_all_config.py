""" Initially want to add publisher to all config yaml file

    # can't read in file to dict. Lose all the comments
    # with (infile).open() as stream:
    #     config = yaml.safe_load(stream)
    # print(config)

ELD
5/15/2025
"""
from __future__ import annotations

from pathlib import Path


def add_publisher(file_path: Path) -> str:
    """ add a tag for publisher so we can switch it to 'iser' when needed """
    # read/write lines
    new_config = ''
    with Path.open(file_path, 'r') as file:
        for line in file:
            if line.startswith("  publisher"):
                print(f'{file_path} has already been processed. No changes made.\n')  # noqa: T201
                return "done"
            if line.startswith("  sources:"):
                new_config += "  publisher: acep\n"
                new_config += line
            else:
                new_config += line
    return new_config


def main() -> None:

    # testing with the template file
    infile = Path(__file__).parents[2] / "config" / "config_template.yml"
    # infile = Path(__file__).parents[3] / "test.yml"
    # outfile = "test.yml"
    new_config = add_publisher(infile)
    if new_config != "done":
        print(f'Writing new {infile}.\n')  # noqa: T201
        with Path.open(infile, 'w') as file:
            file.write(new_config)

    print('\nAltering configuration files:')  # noqa: T201
    proc_dir  = Path(__file__).parents[3] / "src" / "config"
    for type in proc_dir.iterdir():
        if type.is_file():
            # the template file
            continue
        subdir = proc_dir / type
        for file_path in subdir.iterdir():
            if file_path.is_file() and file_path.suffix == '.yml':
                new_config = add_publisher(file_path)
                if new_config != "done":
                    print(f'Writing new {file_path}.\n')  # noqa: T201
                    with Path.open(file_path, 'w') as file:
                        file.write(new_config)


if __name__ == "__main__":

    main()
