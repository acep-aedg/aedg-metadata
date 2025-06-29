# Metadata Generator for the Alaska Energy Data Gateway (AEDG)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/pre-commit/pre-commit.com/main.svg)](https://results.pre-commit.ci/latest/github/pre-commit/pre-commit.com/main)

A fundamental feature of the newly revised Alaska Energy Data Gateway (AEDG) is the documentation of data sources and products. To maximally make these data Findable, Accessible, Interoperable, and Reusable (FAIR), each data file ingested and produced will be accompanied by a metadata file in a standard format.

To standardize production of this multitude of files, we have implemented a command line
tool written in Python. This tool utilizes the [OEMetadata standard](https://openenergyplatform.github.io/oemetadata/latest/), an extension of [Frictionless Data Packages](https://datapackage.org):

Hülk, Ludwig, Jonas Huber, Christian Hofmann, and Christoph Muschner. “Open Energy Family - Open Energy Metadata (OEMetadata).” Python, January 2025. [https://github.com/OpenEnergyPlatform/oemetadata].

Hülk, Ludwig, Jonas Huber, Christian Hofmann, and Christoph Muschner. “Open Energy Metadata (OEMetadata),” March 13, 2025. [https://doi.org/10.5281/zenodo.15019562].

## Installation

This packages uses `pyproject.toml` to define the dependencies instead of `requirements.txt`. It was set-up using `uv` which is the preferred package management system, but pip with `virtualenv` can also be used.

Extra dependencies needed for rendering sphinx documentation (`docs`) and testing with `pytest` (`test`) are defined using optional dependencies and not groups. This is because compatibility with `pip` was important. As of 3/23/2025, `uv` was able to make "groups", but the most recent version of `pip` (v25.0.1) did not have groups enabled yet (v25.1dev seems to). Installation instructions for these extras are included.

Clone the repository locally:

``` shell
% git clone git@github.com:acep-aedg/aedg-metadata.git
% cd aedg-metadata
```

### `uv`

`uv sync` will create the `.venv/` directory and it can also include the optional dependencies too.

``` shell
% uv sync --all-extras  # Include all optional dependencies.
% source .venv/bin/activate
```

### `pip`

``` shell
% python -m venv .venv
% source .venv/bin/activate
% pip install -e .
% pip install '.[test]'
% pip install '.[docs]'
```

### Testing installation

To check the package installed correctly: `aedg_metadata generate --help`

To check the testing installed correctly: `pytest`

To run all the pre-commit checks: `uvx nox`

To render the documentation:

``` shell
% cd docs
% make html
```

## Project Information

### Funding

This project was built with support from State of Alaska capital appropriations for the Alaska Energy Data Gateway.

### Additional Information

Learn more about the [Alaska Center for Energy and Power](https://www.uaf.edu/acep/about/index.php).

The Alaska Energy Data Gateway (AEDG) team has written several Google Docs to support development of the system. Access to these documents is restricted to team members, though the hope is to make them public-facing eventually. The following links are to requirements documentation created during the development of AEDG:

1. [20250220- AEDG Requirements - Metadata](https://docs.google.com/document/d/1UvnJrGbs_hEIAytj6iPVVncXPNA1Xmo7xmFHW7Yce5U/edit?usp=drive_link): This doc analyses how metadata would be used to satisfy user stories and technical needs. The results of this analysis led to the identification of Open Energy Metadata as the best metadata standard to follow.
2. [AEDG Metadata Style Guide](https://docs.google.com/document/d/1xM20wqkLpvIDdac0S7LhYqFY6MSWVQMLe8jMyhSjkec/edit?usp=drive_link): As metadata began to be accumulated, it became apparent that a style guide was needed to standardize language and tone. This doc is under development.
3. [2025-04-15 Keywords Requirements for Search](https://docs.google.com/document/d/1zyfX0OqlclQjHL-16zimbpe6uR_ZOozA9Fe-qcJSdpg/edit?usp=drive_link): In the long term, a standard vocabulary will be used to guide selection of keywords in the metadata. This doc describes how search works in AEDG in hopes of guiding that future discussion.
