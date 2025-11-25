---
layout: page
title: Getting Started
permalink: /getting-started/
nav_order: 3
---

# Getting started

There are several elements needed in order to generating metadata with this system:

1. This code, installed according to the [installation instructions](https://github.com/acep-aedg/aedg-metadata#) with its dependencies.
2. A YAML configuration file that describes the data file being described.
3. The YAML configuration files that define the source data used to pull raw data from the source APIs.
4. The suite of [registry files](/registries) that define the definitions of fields, license, agents etc.

## Configuration Files

The configuration file "hardcodes" options for describing the data file. It is written in [YAML](https://yaml.org/spec/1.2.2/) to be concise and human readable (if it was written in JSON, we might as well write the metadata by hand). It is read in by the system; some of its content links to the real values in the registries, while other content is input verbatum into the output metadata.

The format is roughly a flattened version of the `resource` section of OEMetadata using the same tags. Hopefully, these similarities make it intuitive to fill in the fields.
