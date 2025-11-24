---
layout: page
title: Getting Started
permalink: /getting-started/
nav_order: 2
---

# Getting started

There are several elements to generating metadata with this system:

1. This code, installed according to the [installation instructions](index) with its dependencies.
2. A [YAML configuration file](#configuration-files) that describes the data file being described.
3. The suite of [registry files](./registries.md) that define the definitions of fields, license, agents etc.

## Configuration Files

The configuration file "hardcodes" options for describing the data file. Its name and position are governed by the [implicit rules](#implicit-rules) defined for AEDG. It is written in [YAML](https://yaml.org/spec/1.2.2/) to be concise and human readable (if it was written in JSON, we might as well write the metadata by hand). It is read in by the system; some of its content links to the real values in the registries, while other content is input verbatum into the output metadata.

The format is roughly a flattened version of the `resource` section of OEMetadata using the same tags. Hopefully, these similarities make it intuitive to fill in the fields.

Under development: a script to generate the configuration file from a template so you don't have to copy the existing example, `public_communities_monthly_generation.yml`

## Example Usage

The CLI is set-up according to `typer's` [Building a Package](https://typer.tiangolo.com/tutorial/package/#try-your-cli-program) instructions
so the usage conforms to `aedg_metadata [OPTIONS] COMMAND [ARGS]...`

``` shell
% aedg_metadata generate public_communities_monthly_generation -d public --bbox infer --save
% aedg_metadata generate --help

 Usage: aedg_metadata generate [OPTIONS] CONFIG

 To call gen_meta.py.

╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    config      TEXT  File stem of config file (req). [default: None] [required]                                                                                                                           │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --directory        -d                TEXT                       Subdirectory of data/ where target file lives in the AEDG pond. [default: public]                                                           │
│ --data-dictionary  -dd               TEXT                       Filename of the data dictionary stashed with the data file. If not specified, use the default fields registry file.                         │
│ --bbox             -b                [infer|calc|specify|none]  How the spatial bounding box should be determined. [default: specify]                                                                       │
│ --time             -t                [infer|calc|specify|none]  How the temporal description should be determined. [default: specify]                                                                       │
│ --save                  --no-save                               Write generated metadata to the file or else to the screen. [default: no-save]                                                              │
│ --help                                                          Show this message and exit.                                                                                                                 │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

Note: there is a practice call still hanging around as `aedg_metadata greet Name --count 5`. Don't let that bother you!

## Implicit Rules

We had to make metadata.  Lots of it.  To streamline this, there are rules that restrict this code to context of AEDG only. That isn't optimum, but it saves a lot of trouble as we are getting started. The rules are:

1. There is a single file stem that will be used for both the configuration YAML file and the output JSON metadata file. That stem must match that of the data file being described and is a required argument for `generate`. For instance,
   1. for the data file `capacity.csv`, the stem is `capacity`
   2. configurations file must be called `capacity.yml`
   3. the output metadata will be `capacity.json`
2. The directory structure that contain the input configuration files (`src/config/`) and output metadata files (`metadata/`) must repeat the structure of https://github.com/acep-aedg/aedg-data-pond/tree/main/data. This subdirectory is input as an option of `generate`. For instance:
   1. `capacity.csv` is in the subdirectory `final`
   2. the command is `aedg_metata generate capacity -d final`
   3. `generate` will look to `src/config/final/capacity.yml` for input
   4. `generate` will output `metadata/final/capacity.json`
