---
myst:
  html_meta:
    "description lang=en": |
      Metadata generation for the Alaska Energy Data Gateway.
html_theme.sidebar_secondary.remove: true
---

# Metadata Generator for the Alaska Energy Data Gateway (AEDG)

A fundamental feature of the newly revised Alaska Energy Data Gateway (AEDG) is the
documentation of data sources and products. To maximally make these data Findable, Accessible, Interoperable, and Reusable (FAIR), each data file ingested and produced will
be accompanied by a metadata file in a standard format.

To standardize production of this multitude of files, we have implemented a command line
tool written in Python. This tool utilizes the [OEMetadata standard](#oemetadata-target),
an extension of [Frictionless Data Packages](#datapackage-target).

```{include} ../README.md
:start-after: <!-- SPHINX-START -->
```

## User Guide

```{toctree}
:maxdepth: 2

getting_started
oemetadata
```

## API

Source code for the data pipeline found in `src/aedg_metadata`.

```{toctree}
:maxdepth: 2

API <api/index>
```

## More Information

### Funding

This project was built with support from State of Alaska capital appropriations for the Alaska Energy Data Gateway.

### Additional Information

Learn more about the [Alaska Center for Energy and Power](https://www.uaf.edu/acep/about/index.php).
