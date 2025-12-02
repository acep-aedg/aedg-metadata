---
layout: page
title: Getting Started
permalink: /getting-started/
nav_order: 3
---

# Getting Started

There are several elements needed in order to generating metadata with this system:

1. This code, installed according to the [installation instructions](https://github.com/acep-aedg/aedg-metadata#) with its dependencies.
2. A YAML configuration file that describes the data file being described.
3. The YAML configuration files that define the source data used to pull raw data from the source APIs.
4. The suite of [registry files](/registries) that define the definitions of fields, license, agents etc.

## Configuration Files

The configuration file "hardcodes" options for describing the data file. It is written in [YAML](https://yaml.org/spec/1.2.2/) to be concise and human readable (if it was written in JSON, we might as well write the metadata by hand). It is read in by the system; some of its content links to the real values in the registries, while other content is input verbatum into the output metadata.

The format is roughly a flattened version of the `resource` section of OEMetadata using the same tags. Hopefully, these similarities make it intuitive to fill in the fields.

## Installation in Another Repo
In order to install and run this code from other repositories, we will need to perform some basic set up. First, your repository will need a Python virtual environment with the correct packages installed. Check you Python installation with
`which python`
You should see a response with something like `/Users/yourusername/.pyenv/shims/python`. If not, you may need to install Python. *Caution*: There's a chance that your shell is pointing towards a pre-installed Python, which could cause problems down the road. Best to install a fresh version in a known location.

Next you'll need to create a virtual environment. This can be done by navigating to the root of the repository and running 
`python -m venv venv`

Activate the virtual environment by running 
`source venv/bin/actiate`

Your shell prompt should now have a prefix of `(venv)`, which shows you are ready to install packages in your fresh virtual environment.

In order to install this package, we will use `pip` to install from the github repository. The command looks like this:
`pip install git+https://github.com/acep-aedg/aedg-metadata.git@main#egg=aedg_metadata`

The package should be read and installed to your virtual environment. Check the install by running `aedg_metadata --help`. If all is well you should see an output of various potential commands. Otherwise you may need to go back and rerun the install. Deactivate the environment by running `deactivate`, then burn the virtual environment by running `rm -r venv`

## Running in Another Repo
This package contains a number of moving pieces, and they all need to be located/formatted correctly, otherwise the metadata generator won't run. In particular, you will need:
1. A clear path to your CSV/GeoJSON data (example: `./data/bulk_fuel/bulk_fuel.geojson`)
2. A YAML config file located alongside the data (example: `./data/bulk_fuel/bulk_fuel.yml`)
3. A CSV data dictionary containing fields of the data, located in ./registry (example: `./registry/fields.csv` or `./registry/bulk_fuel_data_dictionary.csv`)
4. A clone of aedg-etl-2024 located somewhere on your machine (example: ~/repos/aedg-etl-2024)

If these requirements are met, you should be able to run the metadata generator for a single file like this:

``` shell
aedg_metadata generate \
    example_data/bulk_fuel/bulk_fuel.geojson \
    ~/repos/aedg-etl-2024/data-sources \
    -dd bulk_fuel_data_dictionary.csv \
    --bbox infer \
    -t specify
```

For sanity, we recommend creating a shell script in your repository (example: ./run_batch.sh) where these individual calls can be run all at once via `./run_batch.sh`.