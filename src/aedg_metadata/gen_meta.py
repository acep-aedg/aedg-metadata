"""Code from the Sandbox Notebook"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from pprint import pprint
from typing import Any

import yaml
from jsonschema import ValidationError, validate
from oemetadata.latest.schema import OEMETADATA_LATEST_SCHEMA
from oemetadata.latest.template import OEMETADATA_LATEST_TEMPLATE


def run_generate(
    file_stem: str,
    flavor: str,
    bbox_type: str,
    write_file: bool
) -> None:
    """Use the class to make and write a new package."""

    new_pkg = AedgOemetadata(file_stem, flavor, bbox_type)
    new_pkg.generate()
    check_schema(new_pkg.data_package)

    if write_file:
        with new_pkg.output_file.open(mode="w") as file:
            json.dump(new_pkg.data_package, file, indent=4)
    else:
        # write output to the screen for debugging
        pprint(new_pkg.data_package, depth=None, sort_dicts=False)  # noqa: T203


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
    """Makes an OEMetadata formatted metadata records and adds AEDG information to it."""

    def __init__(
        self,
        file_stem: str,
        flavor: str,
        bbox_type: str
    ) -> None:
        """Kick off the process by importing the template and config files"""

        file_stem = "public_communities_monthly_generation"

        # Read YAML configuration file
        input_dir = Path(__file__).parents[1] / "config" / flavor
        with (input_dir / f"{file_stem}.yml").open() as stream:
            self.config = yaml.safe_load(stream)

        # Read YAML registry files
        registry_dir = Path(__file__).parents[1] / "registry"
        with (registry_dir / "fields.yml").open() as stream:
            self.fields = yaml.safe_load(stream)
        with (registry_dir / "licenses.yml").open() as stream:
            self.licenses = yaml.safe_load(stream)
        with (registry_dir / "agents.yml").open() as stream:
            self.agents = yaml.safe_load(stream)

        # define the output file
        output_dir = Path(__file__).parents[2] / "metadata" / flavor
        self.output_file = output_dir / f"{file_stem}.json"

        # How shall the bounding box be set?
        self.bbox = bbox_type

        self.data_package = OEMETADATA_LATEST_TEMPLATE.copy()


    def prep_aedg(self) -> None:
        """Make some basic changes that will be true of all AEDG metadata"""

        resource = self.data_package["resources"][0]

        # None are at a single spatial location
        resource["spatial"].pop("location", None)
        # None are gridded
        resource["spatial"]["extent"].pop("resolutionValue", None)
        resource["spatial"]["extent"].pop("resolutionUnit", None)
        # Won't be using a path or URI to a specific location (Wikidata or OpenStreetMap)
        resource["spatial"]["extent"].pop("@id", None)
        # None are embargoed
        resource.pop("embargoPeriod", None)
        # everything is in US english
        resource["languages"] = ["en-US"]
        # publishing today
        resource["publicationDate"] = f"{date.today()}"
        # we aren't using the OEMetadata review system
        resource.pop("review", None)
        # CSV files will always be comma delimited
        resource["dialect"]["delimiter"] = ","
        # We use "." in our floating point numbers
        resource["dialect"]["decimalSeparator"] = "."
        # ACEP is a contributor to all (fill in details later)
        resource["contributors"] = [
            {
                "path": "https://github.com/acep-aedg/aedg-etl-2024",
                "organization": "Alaska Center for Energy and Power, University of Alaska Fairbanks",
                "date": f"{date.today()}",
                "object": "[Fill in object of the change]",
                "comment": "[Fill in how it was changed]",
            }
        ]
        # Context is AEDG
        resource["context"] = {
            "title": "Alaska Energy Data Gateway",
            "homepage": "https://akenergygateway.alaska.edu/",
            "publisher": "Alaska Center for Energy and Power, University of Alaska Fairbanks",
            "fundingAgency": "State of Alaska",
        }

        # One day we will do Ontology, but this is not the day :(
        resource.pop("subject", None)
        resource["schema"]["fields"][0].pop("isAbout", None)
        resource["schema"]["fields"][0].pop("valueReference", None)

        self.data_package["resources"][0] = resource

    def apply_config(self) -> None:
        """Copy in configs specific to this file"""

        self.data_package["name"] = self.config["metadata"]["name"]
        self.data_package["title"] = self.config["metadata"]["title"]
        self.data_package["description"] = self.config["metadata"]["description"]

        # there is only 1 resource and it is same as the package
        resource = self.data_package["resources"][0]
        resource["name"] = self.config["metadata"]["name"]
        resource["title"] = self.config["metadata"]["title"]
        resource["description"] = self.config["metadata"]["description"]

        # add keywords
        resource["keywords"] = self.config["metadata"]["resources"][0]["keywords"]
        resource["topics"] = self.config["metadata"]["resources"][0]["topics"]

        # add info about the file being described
        file_path = self.config["metadata"]["resources"][0]["path"]
        resource["path"] = file_path
        if file_path.endswith(".csv"):
            resource["type"] = "table"
            resource["format"] = "CSV"
        if file_path.endswith(".geojson"):  # I don't know if OEMetadata does this
            resource["type"] = "geospatial"
            resource["format"] = "GEOJOSN"

        self.data_package["resources"][0] = resource

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


    def add_bbox(self) -> None:
        """Add the spatial extent.
        infer: Annotated[str, "Infer the bounding box from the file suffix."] = "infer"
        calc: Annotated[str, "Calculate the bounding box from the GeoJSON."] = "calc"
        specify: Annotated[str, "Specify the bounding box in the config file."] = "specify"
        none: Annotated[str, "Do not include a bounding box."] = "none"
        """

        # prep
        resource = self.data_package["resources"][0]

        if self.bbox == 'none':
            resource.pop('spatial', None)
        else:
            if self.bbox == 'calc':
                # TODO: can pull crs and bounds from file
                bounding_box = []
                crs = "null"
                name = "none"
            elif self.bbox == 'specify':
                bounding_box = self.config["metadata"]["resources"][0]['spatial']["boundingBox"]
                crs = self.config["metadata"]["resources"][0]['spatial']["crs"]
                name = self.config["metadata"]["resources"][0]['spatial']["name"]
            else:  # self.bbox == 'infer'
                # set the geographic bounding box to all of Alaska.
                # The format is [minLon, minLat, maxLon, maxLat] or [W,S,E,N]
                bounding_box = [-187.55, 51.21, -130.0, 71.35]
                crs = "OGC:CRS84"
                name = "Alaska"

            resource["spatial"]["extent"]["boundingBox"] = bounding_box
            resource["spatial"]["extent"]["crs"] = crs
            resource["spatial"]["extent"]["name"] = name

        self.data_package["resources"][0] = resource

    def generate(self) -> None:
        """Run all the steps"""
        self.prep_aedg()
        self.apply_config()
        self.add_license()
        self.add_fields()
        self.add_bbox()


if __name__ == "__main__":

    pass
