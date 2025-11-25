---
layout: page
title: About
permalink: /about/
nav_order: 2
---

# About


## Beginnings
This repository began as a project-specific entity to generate metadata for the [Alaska Energy Data Gateway](https://akenergygateway.alaska.edu) (AEDG) that conformed to the [Open Energy Metadata (OEMetadata)](https://openenergyplatform.github.io/oemetadata/latest/) standard. To that end, the code here was a great success, allowing us to impliment features on the front-end that were built upon reliable and standardized metadata. 

Since that initial success, we have come to realize the applicability of this code outside the context of AEDG. Shouldn't every ACEP project have great metadata to ride alonside the data products? Shouldn't ACEP adopt a single metadata standard across the organization? The answers were **yes**. And so we have begun the task of generalizing the code.

## Generalization
In this repository's initial structure, YAML config files were stored in this repository with a specific directory structure. These config files were used to fetch CSV/GeoJSON data files from the aedg-data-pond repository as well as source config files from the aedg-etl reposotiry. This hardcoding of directory structure and sources was a known limitation, done to get the project up and running. AEDG was a single project, so specific details were less of an issue. Now, as we start to generalize the code for multi-project usage, we assume the best place for metadata config files is right alongside the data itself. To that end, we have changed the CLI to require a path to the data file, which is assumed to be located alongside a config file sharing the same name. The generated JSON metadata of the same name will be outputted to this location. 
