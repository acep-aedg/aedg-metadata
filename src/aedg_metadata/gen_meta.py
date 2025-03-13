"""Code from the Sandbox Notebook"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import yaml
from jsonschema import ValidationError, validate
from oemetadata.latest.schema import OEMETADATA_LATEST_SCHEMA
from oemetadata.latest.template import OEMETADATA_LATEST_TEMPLATE

CONFIG_FILE = "../config/public/public_communities_monthly_generation.yml"
METADATA_FILE = "../../metadata/public/public_communities_monthly_generation.json"


def check_schema(package: dict) -> None:
    """Function from OEMetadata to check schema against standard"""
    try:
        validate(package, OEMETADATA_LATEST_SCHEMA)
        print("Metadata is valid according to OEMetadata Schema (Latest).")  # noqa: T201
    except ValidationError as e:
        print(  # noqa: T201
            "Cannot validate the metadata according to OEMetadata Schema (Latest)!", e
        )


def prep_aedg(new_pkg: dict) -> dict:
    """Make some basic changes that will be true of all AEDG metadata"""

    # None are at a single spatial location
    new_pkg["resources"][0]["spatial"].pop("location", None)
    # None are embargoed
    new_pkg["resources"][0].pop("embargoPeriod", None)
    # everything is in US english
    new_pkg["resources"][0]["languages"] = ["en-US"]
    # publishing today
    new_pkg["resources"][0]["publicationDate"] = f"{date.today()}"
    # we aren't using the OEMetadata review system
    new_pkg["resources"][0].pop("review", None)
    # CSV files will always be comma delimite
    new_pkg["resources"][0]["dialect"]["delimiter"] = ","
    # We use "." in our floating point numbers
    new_pkg["resources"][0]["dialect"]["decimalSeparator"] = "."
    # ACEP is a contributor to all (fill in details later)
    new_pkg["resources"][0]["contributors"] = [
        {
            "path": "https://github.com/acep-aedg/aedg-etl-2024",
            "organization": "Alaska Center for Energy and Power, University of Alaska Fairbanks",
            "date": f"{date.today()}",
            "object": "[Fill in object of the change]",
            "comment": "[Fill in how it was changed]",
        }
    ]
    # Context is AEDG
    new_pkg["resources"][0]["context"] = {
        "title": "Alaska Energy Data Gateway",
        "homepage": "https://akenergygateway.alaska.edu/",
        "publisher": "Alaska Center for Energy and Power, University of Alaska Fairbanks",
        "fundingAgency": "State of Alaska",
    }

    # One day we will do Ontology, but this is not the day :(
    new_pkg["resources"][0].pop("subject", None)
    new_pkg["resources"][0]["schema"]["fields"][0].pop("isAbout", None)
    new_pkg["resources"][0]["schema"]["fields"][0].pop("valueReference", None)

    return new_pkg


def apply_config(new_pkg: dict, config: dict) -> dict:
    """Copy in configs specific to this file"""

    new_pkg["name"] = config["metadata"]["name"]
    new_pkg["title"] = config["metadata"]["title"]
    new_pkg["description"] = config["metadata"]["description"]

    # resource is same as the package, I guess
    new_pkg["resources"][0]["name"] = config["metadata"]["name"]
    new_pkg["resources"][0]["title"] = config["metadata"]["title"]
    new_pkg["resources"][0]["description"] = config["metadata"]["description"]
    new_pkg["resources"][0]["keywords"] = config["metadata"]["resources"][0]["keywords"]
    new_pkg["resources"][0]["topics"] = config["metadata"]["resources"][0]["topics"]
    new_pkg["resources"][0]["path"] = config["metadata"]["resources"][0]["path"]
    if config["metadata"]["resources"][0]["path"].endswith(".csv"):
        new_pkg["resources"][0]["type"] = "table"
        new_pkg["resources"][0]["format"] = "CSV"
    if config["metadata"]["resources"][0]["path"].endswith(
        ".geojson"
    ):  # I don't know if OEMetadata does this
        new_pkg["resources"][0]["type"] = "geospatial"
        new_pkg["resources"][0]["format"] = "GEOJOSN"

    return new_pkg


def add_license(new_pkg: dict, config: dict, licenses: dict) -> dict:
    """Add the license"""

    all_licenses = []
    for license_tag in config["metadata"]["resources"][0]["licenses"]:
        license = {"name": license_tag}
        license.update(licenses["licenses"][license_tag])
        all_licenses.append(license)

    if len(all_licenses) > 0:
        # replace the empty template field
        new_pkg["resources"][0]["licenses"] = all_licenses
    else:
        # remove the empty template field
        new_pkg["resources"][0].pop("resources", None)

    return new_pkg


def add_fields(new_pkg: dict, config: dict, fields: dict) -> dict:
    """Add the fields"""

    # don't care about the distinction between index and value columns here
    all_fields = fields["fields"]["idxcols"].copy()
    all_fields.update(fields["fields"]["cols"])

    all_schemas = []
    field_names = config["metadata"]["resources"][0]["fields"]
    for field_name in field_names:
        assert field_name in all_fields
        schema = {"name": field_name}
        schema.update(all_fields[field_name])
        all_schemas.append(schema)

    assert len(all_schemas) > 0
    # replace the empty template field
    new_pkg["resources"][0]["schema"]["fields"] = all_schemas
    return new_pkg


if __name__ == "__main__":
    check_schema(OEMETADATA_LATEST_TEMPLATE)

    # Read YAML files
    with Path(CONFIG_FILE).open() as stream:
        config = yaml.safe_load(stream)

    with Path("../registry/fields.yml").open() as stream:
        fields = yaml.safe_load(stream)

    with Path("../registry/licenses.yml").open() as stream:
        licenses = yaml.safe_load(stream)

    with Path("../registry/agents.yml").open() as stream:
        agents = yaml.safe_load(stream)

    data_package = prep_aedg(OEMETADATA_LATEST_TEMPLATE.copy())
    data_package = apply_config(data_package, config)
    data_package = add_license(data_package, config, licenses)
    data_package = add_fields(data_package, config, fields)
    check_schema(data_package)

    with Path(METADATA_FILE).open(mode="w") as file:
        json.dump(data_package, file, indent=4)
