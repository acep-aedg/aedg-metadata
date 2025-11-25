---
layout: page
title: Getting Started
permalink: /getting-started/
nav_order: 3
---

# Getting started

There are several elements needed in order to generating metadata with this system:

1. This code, installed according to the [installation instructions](https://github.com/acep-aedg/aedg-metadata#) with its dependencies.
2. A [YAML configuration file](#configuration-files) that describes the data file being described.
3. The suite of [registry files](./registries.md) that define the definitions of fields, license, agents etc.

## Configuration Files

The configuration file "hardcodes" options for describing the data file. It is written in [YAML](https://yaml.org/spec/1.2.2/) to be concise and human readable (if it was written in JSON, we might as well write the metadata by hand). It is read in by the system; some of its content links to the real values in the registries, while other content is input verbatum into the output metadata.

The format is roughly a flattened version of the `resource` section of OEMetadata using the same tags. Hopefully, these similarities make it intuitive to fill in the fields.


## Example Usage

The CLI is set-up according to `typer's` [Building a Package](https://typer.tiangolo.com/tutorial/package/#try-your-cli-program) instructions
so the usage conforms to `aedg_metadata [OPTIONS] COMMAND [ARGS]...`

``` shell
% aedg_metadata generate \
    data/public_fuel_prices/public_fuel_prices.csv \
    ~/repos/aedg-etl-2024/data-sources \
    -dd fields.csv \
    --bbox infer \
    -t specify \
    --save

% aedg_metadata generate --help

 Usage: aedg_metadata generate [OPTIONS] CONFIG

╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    data-path      TEXT  Path to CSV or GeoJSON data (req). [default: None] [required]
│ *    source-dir-path      TEXT  Path to YML configs for upstream data sources listed in config.sources. In the context of AEDG, this is aedg-etl-2024 repo. (req). [default: None] [required]                                                                                                                               │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
                                                          │
│ --data-dictionary  -dd               TEXT                       Filename of the data dictionary stashed with the data file. If not specified, use the default fields registry file.                         │
│ --bbox             -b                [infer|calc|specify|none]  How the spatial bounding box should be determined. [default: specify]                                                                       │
│ --time             -t                [infer|calc|specify|none]  How the temporal description should be determined. [default: specify]                                                                       │
│ --save                  --no-save                               Write generated metadata to the file or else to the screen. [default: no-save]                                                              │
│ --help                                                          Show this message and exit.                                                                                                                 │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

