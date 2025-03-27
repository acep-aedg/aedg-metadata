# Registries

In world of energy metadata, a standout implementation is [Friendly Data](https://github.com/sentinel-energy/friendly_data/tree/master).  This package was developed for the [SENTINEL](https://sentinel.energy/), an energy modeling experiment. Friendly Data was based on Frictionless metadata (not OEMetadata) and seems to have ended a few years ago, but their use of "registry" files to standardize data definitions is very interesting.

AEDG Metadata generation borrows the concept of registries from Friendly Data and implements it in a couple different contexts. These files should be created with care and nurtured because the generation process pulls content from them.

## Fields

Within Frictionless metadata, fields are equivalent to a data dictionary and are nestled within the resource's schema. OEMetadata added a few attributes to the basic Frictionless field. `Fields` was originally implemented as a YAML file (like in Friendly Data) but there are so darn many of them, that it because easier to manage in a CSV file.

Several of the field attributes in OEMetadata refer to the Open Energy Ontology to link the field to a specific definition. We are not using those fields.

Field attributes are:

- name (string)*: name of the field, lowercase alphanumeric characters or underscores
- long_name (string)**: non-standard field for text labels to use within AEDG
- description (string)**: text describing the field
- type(string)*: data type of the field (example: geometry(Point, 4326))
  - from [JSON](https://json-schema.org/understanding-json-schema/reference/type): array, boolean, integer, number, null, object, regular expressions, or string
- nullable (boolean): specify that a column can be nullable. Defaults to True
- unit (string)**: unit of a field. If it does not apply, use 'null'

\* mandatory for OEMetadata

** mandatory for AEDG

## Licenses

Licenses are a standard part of the Frictionless standard. The [Data Package docs](https://datapackage.org/standard/data-package/#licenses) notes that these are not legally binding. License are not required; they are optional and any of the attributes can be omitted.

There is a distinction in OEMetadata between the licenses of the source data and the licenses applied to the described data. This distinction is under development for us. The license registry might have to be updated to account for this.

License attributes are:

- name: A string containing an Open Definition license ID
- path: A URL or Path, that is a fully qualified HTTP address, or a relative POSIX path.
- title: A string containing human-readable title.
- instruction: A short description of rights and obligations. The use of tl;drLegal is recommended.
- attribution: A copyright owner of the data. Must be provided if attribution licenses are used.
- copyrightStatement: A link or path that proves that the data has the appropriate license. This can be a page number or website imprint.

## Agents

This is borrowing a concept used at Axiom Data Science: to create definitions for agents or organizations that can be used within the context of AEDG. These fields do not directly map to concepts within OEMetadata, but can be used in various OEMetadata contexts such as `sources` and `contributions`.

- code (string): code used in configurations
- name (string): the title of the organization
- home_page (string): URL where can find more information on the organization
- description (string): a mission statement or description of the organization to give context

### Sources

`Sources` refers to the origin of the data from which the described data are derived. From the AEDG user stories, this means including information so that:

- Users can go back to the original source to find out more information when they want/need to
- Agencies receive appropriate credit when we use their data in our product

Many AEDG tables are amalgamations of data from multiple sources. So the idea is to have a registry list of each source and then to build this section from them as needed. This idea is under development. It remains to be seen how to map required `source` attributes to the agents.

Source attributes are:

- title: A string containing a title of the source (e.g. document or organization name).
- authors: An array of the full names of authors of the source material.
- description: Free text description of the source.
- publicationYear: the year when the work was published.
- path: A URL or Path, that is a fully qualified HTTP address, or a relative POSIX path.

## Keywords

Under development

## Topics

Under development
