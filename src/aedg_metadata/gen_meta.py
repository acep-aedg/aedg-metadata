"""Code from the Sandbox Notebook"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

import yaml
from jsonschema import ValidationError, validate
from oemetadata.latest.schema import OEMETADATA_LATEST_SCHEMA
from oemetadata.latest.template import OEMETADATA_LATEST_TEMPLATE

CONFIG_FILE = "../config/public/public_communities_monthly_generation.yml"
METADATA_FILE = "../../metadata/public/public_communities_monthly_generation.json"


def check_schema(package: dict[Any, Any]) -> None:
    """Function from OEMetadata to check schema against standard"""
    try:
        validate(package, OEMETADATA_LATEST_SCHEMA)
        print("Metadata is valid according to OEMetadata Schema (Latest).")  # noqa: T201
    except ValidationError as e:
        print(  # noqa: T201
            "Cannot validate the metadata according to OEMetadata Schema (Latest)!", e
        )


class AedgOemetadata:
    """
    Attributes
    ----------
    config: dict
        configuration info for metadata generation
    package: dict
        data package metadata conforming to the OEMetadata standard
    """
    def __init__(self) -> None:
        """Kick off the process by importing the template and config files"""
        # Read YAML files
        with Path(CONFIG_FILE).open() as stream:
            self.config = yaml.safe_load(stream)

        with Path("../registry/fields.yml").open() as stream:
            self.fields = yaml.safe_load(stream)
        with Path("../registry/licenses.yml").open() as stream:
            self.licenses = yaml.safe_load(stream)
        with Path("../registry/agents.yml").open() as stream:
            self.agents = yaml.safe_load(stream)

        # set a geographic bounding box for all of Alaska
        # The covered area specified by the coordinates of a bounding box.
        # The format is [minLon, minLat, maxLon, maxLat] or [W,S,E,N].
        self.all_alaska_bb = [-187.55, 51.21, -130.0, 71.35]

        self.data_package = OEMETADATA_LATEST_TEMPLATE.copy()


    def prep_aedg(self) -> None:
        """Make some basic changes that will be true of all AEDG metadata"""

        # None are at a single spatial location
        self.data_package["resources"][0]["spatial"].pop("location", None)
        # None are gridded
        self.data_package["resources"][0]["spatial"]["extent"].pop("resolutionValue", None)
        self.data_package["resources"][0]["spatial"]["extent"].pop("resolutionUnit", None)
        # Won't be using a path or URI to a specific location (Wikidata or OpenStreetMap)
        self.data_package["resources"][0]["spatial"]["extent"].pop("@id", None)
        # None are embargoed
        self.data_package["resources"][0].pop("embargoPeriod", None)
        # everything is in US english
        self.data_package["resources"][0]["languages"] = ["en-US"]
        # publishing today
        self.data_package["resources"][0]["publicationDate"] = f"{date.today()}"
        # we aren't using the OEMetadata review system
        self.data_package["resources"][0].pop("review", None)
        # CSV files will always be comma delimited
        self.data_package["resources"][0]["dialect"]["delimiter"] = ","
        # We use "." in our floating point numbers
        self.data_package["resources"][0]["dialect"]["decimalSeparator"] = "."
        # ACEP is a contributor to all (fill in details later)
        self.data_package["resources"][0]["contributors"] = [
            {
                "path": "https://github.com/acep-aedg/aedg-etl-2024",
                "organization": "Alaska Center for Energy and Power, University of Alaska Fairbanks",
                "date": f"{date.today()}",
                "object": "[Fill in object of the change]",
                "comment": "[Fill in how it was changed]",
            }
        ]
        # Context is AEDG
        self.data_package["resources"][0]["context"] = {
            "title": "Alaska Energy Data Gateway",
            "homepage": "https://akenergygateway.alaska.edu/",
            "publisher": "Alaska Center for Energy and Power, University of Alaska Fairbanks",
            "fundingAgency": "State of Alaska",
        }

        # One day we will do Ontology, but this is not the day :(
        self.data_package["resources"][0].pop("subject", None)
        self.data_package["resources"][0]["schema"]["fields"][0].pop("isAbout", None)
        self.data_package["resources"][0]["schema"]["fields"][0].pop("valueReference", None)

    def apply_config(self) -> None:
        """Copy in configs specific to this file"""

        self.data_package["name"] = self.config["metadata"]["name"]
        self.data_package["title"] = self.config["metadata"]["title"]
        self.data_package["description"] = self.config["metadata"]["description"]

        # resource is same as the package, I guess
        self.data_package["resources"][0]["name"] = self.config["metadata"]["name"]
        self.data_package["resources"][0]["title"] = self.config["metadata"]["title"]
        self.data_package["resources"][0]["description"] = self.config["metadata"]["description"]

        # add keywords
        self.data_package["resources"][0]["keywords"] = self.config["metadata"]["resources"][0]["keywords"]
        self.data_package["resources"][0]["topics"] = self.config["metadata"]["resources"][0]["topics"]

        # add info about the file being described
        file_path = self.config["metadata"]["resources"][0]["path"]
        self.data_package["resources"][0]["path"] = file_path
        if file_path.endswith(".csv"):
            self.data_package["resources"][0]["type"] = "table"
            self.data_package["resources"][0]["format"] = "CSV"
        if file_path.endswith(".geojson"):  # I don't know if OEMetadata does this
            self.data_package["resources"][0]["type"] = "geospatial"
            self.data_package["resources"][0]["format"] = "GEOJOSN"

        # add spatial extents - TODO: split into own function if it gets too complicated
        bounding_box = self.config["metadata"]["resources"][0]['spatial']["boundingBox"]
        crs = self.config["metadata"]["resources"][0]['spatial']["crs"]
        if self.data_package["resources"][0]["format"] == "CSV":
            if not crs:
                crs = "null"
            if not bounding_box:
                bounding_box = self.all_alaska_bb
                name = "Alaska"
        if self.data_package["resources"][0]["format"] == "GEOJSON":
            # TODO: can pull crs and bounds from file
            pass
        self.data_package["resources"][0]["spatial"]["extent"]["boundingBox"] = bounding_box
        self.data_package["resources"][0]["spatial"]["extent"]["crs"] = crs
        if name:
            self.data_package["resources"][0]["spatial"]["extent"]["name"] = name



    def add_license(self) -> None:
        """Add the license"""

        all_licenses = []
        for license_tag in self.config["metadata"]["resources"][0]["licenses"]:
            license = {"name": license_tag}
            license.update(self.licenses["licenses"][license_tag])
            all_licenses.append(license)

        if len(all_licenses) > 0:
            # replace the empty template field
            self.data_package["resources"][0]["licenses"] = all_licenses
        else:
            # remove the empty template field
            self.data_package["resources"][0].pop("resources", None)


    def add_fields(self) -> None:
        """Add the fields"""

        # don't care about the distinction between index and value columns here
        all_fields = self.fields["fields"]["idxcols"].copy()
        all_fields.update(self.fields["fields"]["cols"])

        all_schemas = []
        field_names = self.config["metadata"]["resources"][0]["fields"]
        for field_name in field_names:
            assert field_name in all_fields
            schema = {"name": field_name}
            schema.update(all_fields[field_name])
            all_schemas.append(schema)

        assert len(all_schemas) > 0
        # replace the empty template field
        self.data_package["resources"][0]["schema"]["fields"] = all_schemas


    def generate(self) -> None:
        """Run all the steps"""
        self.prep_aedg()
        self.apply_config()
        self.add_license()
        self.add_fields()


if __name__ == "__main__":

    new_pkg = AedgOemetadata()
    new_pkg.generate()
    check_schema(new_pkg.data_package)

    with Path(METADATA_FILE).open(mode="w") as file:
        json.dump(new_pkg.data_package, file, indent=4)
