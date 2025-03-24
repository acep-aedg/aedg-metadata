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
    bbox_opt: str,
    temporal_opt: str,
    write_file: bool
) -> None:
    """Use the class to make and write a new package."""

    new_pkg = AedgOemetadata(file_stem, flavor)
    new_pkg.generate(bbox_opt, temporal_opt)
    check_schema(new_pkg.data_package)

    if write_file:
        with new_pkg.output_file.open(mode="w") as file:
            json.dump(new_pkg.data_package, file, indent=4)
            # for pre-commit end of file check
            file.write("\n")
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
        # Only 1 file, so there should be no keys referring to other tables
        resource["schema"].pop("foreignKeys", None)

        self.data_package["resources"][0] = resource

    def apply_config(self) -> None:
        """Copy in configs specific to this file"""

        self.data_package["name"] = self.config["resource"]["name"]
        self.data_package["title"] = self.config["resource"]["title"]
        self.data_package["description"] = self.config["resource"]["description"]

        # there is only 1 resource and it is same as the package
        resource = self.data_package["resources"][0]
        resource["name"] = self.config["resource"]["name"]
        resource["title"] = self.config["resource"]["title"]
        resource["description"] = self.config["resource"]["description"]

        # add keywords
        resource["keywords"] = self.config["resource"]["keywords"]
        resource["topics"] = self.config["resource"]["topics"]

        # add info about the file being described
        file_path = self.config["resource"]["path"]
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
        for license_tag in self.config["resource"]["licenses"]:
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
        """Add the fields and designate the primary keys."""

        # the registry fields is a dictionary of dictionaries
        reg_fields = self.fields["fields"]
        con_fields = self.config["resource"]["fields"]
        fields = []
        for field_name in con_fields:
            assert field_name in reg_fields
            field = {"name": field_name}
            field.update(reg_fields[field_name])
            fields.append(field)

        assert len(fields) > 0
        self.data_package["resources"][0]["schema"]["fields"] = fields

        # add the primary keys from the config file - if they are described already
        primaryKeys = self.config["resource"]["primaryKey"]
        assert set(primaryKeys).issubset(set(con_fields))
        self.data_package["resources"][0]["schema"]["primaryKey"] = primaryKeys

    def add_bbox(self, bbopt: str) -> None:
        """Add the spatial extent.
        infer: Annotated[str, "Infer the bounding box from the file suffix."] = "infer"
        calc: Annotated[str, "Calculate the bounding box from the GeoJSON."] = "calc"
        specify: Annotated[str, "Specify the bounding box in the config file."] = "specify"
        none: Annotated[str, "Do not include a bounding box."] = "none"
        """

        # prep
        resource = self.data_package["resources"][0]
        fields = {'name', 'boundingBox', 'crs'}

        if bbopt == 'none':
            resource.pop('spatial', None)
        elif bbopt == 'calc':
            # TODO: can pull crs and bounds from file
            pass
        elif bbopt == 'specify':
            spatial = self.config["resource"]["spatial"]
            # check that all the keys are present
            assert set(spatial.keys()) == fields
            resource["spatial"]["extent"] = spatial
        else:  # bbopt == 'infer'
            # set the geographic bounding box to all of Alaska.
            # The format is [minLon, minLat, maxLon, maxLat] or [W,S,E,N]
            resource["spatial"]["extent"]["name"] = "Alaska"
            resource["spatial"]["extent"]["bounding_box"] = [-187.55, 51.21, -130.0, 71.35]
            resource["spatial"]["extent"]["crs"] = "OGC:CRS84"

        self.data_package["resources"][0] = resource

    def add_temporal(self, topt: str) -> None:
        """Add the temporal characteristics.
        infer: Annotated[str, "Set a default temporal description."] = "infer"
        calc: Annotated[str, "Calculate the temporal bounds from the file."] = "calc"
        specify: Annotated[str, "Specify the temporal description in the config file."] = "specify"
        none: Annotated[str, "Do not include temporal information."] = "none"
        """

        # prep
        resource = self.data_package["resources"][0]
        fields = {'start', 'end', 'resolutionValue', 'resolutionUnit', 'alignment', 'aggregationType'}

        if topt == 'none':
            resource.pop('temporal', None)
        elif topt == 'calc':
            # TODO: can pull timeseries info from file
            pass
        elif topt == 'specify':
            resource["temporal"]["referenceDate"] = self.config["resource"]["temporal"]["referenceDate"]
            # OEMetadata standard includes possibility of multiple time periods
            # i.e. it is a list
            resource["temporal"]["timeseries"] = []
            for timeseries in self.config["resource"]["temporal"]["timeseries"]:
                period = {}
                # check that all the keys are present
                assert set(timeseries.keys()) == fields
                # but some of them might be null, so pop them off
                for key in timeseries:
                    if timeseries[key]:
                        period[key] = timeseries[key]
                resource["temporal"]["timeseries"].append(period)
        else:  # topt == 'infer'
            # assume it is not a timeseries, but it has an as_of_date (set arbitrarily for now)
            resource["temporal"]["referenceDate"] = "2025-01-01"
            resource["temporal"].pop("timeseries")

        self.data_package["resources"][0] = resource

    def generate(self, bbopt: str, topt: str) -> None:
        """Run all the steps"""
        self.prep_aedg()
        self.apply_config()
        self.add_license()
        self.add_fields()
        self.add_bbox(bbopt)
        self.add_temporal(topt)


if __name__ == "__main__":

    pass
