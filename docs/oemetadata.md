---
layout: page
title: Open Energy Metadata
permalink: /oemedata/
nav_order: 3
---


# Metadata Overview

Metadata describes data so that is useful beyond the context for which the dataset was originally created. We want other people to use the data we’ve posted in Alaska Energy Data Gateway (AEDG), so we include metadata to answer the questions these potential future users might have. Metadata describes the what, where, when, how of data collection and other useful information like the units and contact information of the data collector.

Metadata can be a simple text file, but AEDG also uses the metadata to build web pages. That means the encoded information must be readable to display it properly. To enable that, the metadata is written according to an agreed upon standard format. For our metadata standard, we decided to use [Open Energy Metadata (OEMetadata)](https://openenergyplatform.github.io/oemetadata/latest/), which is an offshoot of [Frictionless Data Packages](https://frictionlessdata.io/).


## Data Packages / Frictionless

AEDG follows the Data Package schema with the constraint that only a single resource (table) is described in each file. This provides the basis for describing fundamental features such as variable descriptions (data dictionary), data sources, contributors, and licenses in a standard, accessible manner. The data dictionary is contained in a section within `resources` called `schema`.

### Data Package

> [Data Package](https://datapackage.org/) is a standard consisting of a set of simple yet extensible specifications to describe datasets, data files and tabular data. It is a data definition language (DDL) and data API that facilitates findability, accessibility, interoperability, and reusability (FAIR) of data.

There are schemas to define the [Data Package](https://datapackage.org/standard/data-package), each [Data Resource](https://datapackage.org/standard/data-resource) in the package, and a [Table Schema](https://datapackage.org/standard/table-schema) to use with CSV files. These schemas follow the [JSON Schema](https://json-schema.org) specification which enables consistency and validation checks.

The Alaska Center for Energy and Power (ACEP) has previously used this standard in the following projects:

- Downloadable data tables in the [2024 Alaska Electricity Trends Report](https://acep-uaf.github.io/aetr-web-book-2024/data.html).
- Downloadable packages of data in the [Alaska Power Cost Equalization (PCE) Utility Monthly Reports (UMR) Database](https://acep-uaf.github.io/pce-database/downloads.html) (under development)

### Frictionless

Frictionless is a framework for managing Data Packages that has been implemented in many languages:

- For Python, [frictionless-py](https://framework.frictionlessdata.io/) includes a library of tools and a CLI with a nicely complete set of [GitHub documentation](https://framework.frictionlessdata.io/).
- If you prefer R, there is an [frictionless R package](https://docs.ropensci.org/frictionless/) too with an [R tutorial](https://cran.r-project.org/web/packages/frictionless/vignettes/frictionless.html).
- On the display side, there are [Javascript React components](https://github.com/frictionlessdata/datapackage-render-js)

One advantage of Frictionless is its ability to validate your files against the published schema.  Here is how you can do it in Python:

``` python
from frictionless import validate
print(validate('table.csv', schema='schema.json'))
# or
package.validate()
```

There is also a command line interface which you would invoke with:

``` shell
% frictionless validate capital-invalid.csv
```

## OEMetadata

There were many other descriptions we wanted to add to our data that are not included in the Data Package standard. For instance, we wanted to include information about position, time, and units while leaving open the possibility of connecting with standard variables definitions. To include these elements, we utilized an extension of the Data Package standard developed by the [Open Energy Platform](https://openenergyplatform.org/): Open Energy Metadata, or OEMetadata, for short.

### Benefits

Besides the additional fields, there are other benefits to our adoption of this standard for energy data.

1. It is an extension of the well-defined, simple metadata standard Data Packages.
2. Open Energy Platform published mapping between [OEMetadata and DCAT-AP](https://openenergyplatform.github.io/oemetadata/2.0/metadata/metadata_mappings/), which is the other standard we were seriously considering.
3. The extensions they added align with the fields we required for AEDG, namely: spatial and temporal bounds and more complete documentation of sources. But the standard remains simple, without extra fields we had no interest in.
4. It has built-in connections to Open Energy Platform's standard vocabulary [Open Energy Ontology](https://openenergy-platform.org/ontology/) for when we are ready to standardize keywords.
5. The project is open source. The GitHub repository [oemetadata](https://github.com/OpenEnergyPlatform/oemetadata)  contains metadata templates, schemas, and example validation code that can be installed for local use via a pip package.

### References

- [OEMetadata Schema](https://github.com/OpenEnergyPlatform/oemetadata/blob/develop/oemetadata/latest/schema.json)
- [OEMetadata Template](https://github.com/OpenEnergyPlatform/oemetadata/blob/develop/oemetadata/latest/template.json)
- Hülk, Ludwig, Jonas Huber, Christian Hofmann, and Christoph Muschner. “Open Energy Family - Open Energy Metadata (OEMetadata).” Python, January 2025. <https://github.com/OpenEnergyPlatform/oemetadata>.
- Hülk, Ludwig, Jonas Huber, Christian Hofmann, and Christoph Muschner. “Open Energy Metadata (OEMetadata),” March 13, 2025. <https://doi.org/10.5281/zenodo.15019562>.

### Additional Resources

Open Energy Platform distributes additional tools, including:

- an authoring tool: [oemetabuilder](https://openenergyplatform.org/dataedit/oemetabuilder/) which is a fillable form
- a conversion tool: [omi](https://omi.readthedocs.io/en/latest/)
- [tutorials](https://openenergyplatform.github.io/academy/tutorials) on its use

Because OEMetadata is compliant with Data Packages, it is possible to download fully described data from their database as a Data Package. See this example of the download options on the Open Energy Platform's expression of the [Windzone map for Germany](https://openenergyplatform.org/dataedit/view/climate/rli_dibt_windzone):

![image](/assets/img/oeplatform_screenshot.png)
