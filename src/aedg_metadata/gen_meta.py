"""Code to generate metadata for AEDG starting from the OEMetadata template"""

from __future__ import annotations

import json
from copy import deepcopy
from datetime import date
from pathlib import Path

import pandas as pd
import yaml
from oemetadata.latest.template import OEMETADATA_LATEST_TEMPLATE

from aedg_metadata import ExtentTypes

from .helpers import check_fields, check_schema, parse_combined_header


def run_generate(
    data_path: str | Path,
    sources_dir_path: str | Path,
    data_dictionary: str,
    bbox_opt: ExtentTypes,
    temporal_opt: ExtentTypes,
) -> AedgOemetadata:
    """Use the class to make a new package."""

    print(f"\nProcessing: {Path(data_path).stem}")  # noqa: T201
    new_pkg = AedgOemetadata(data_path, sources_dir_path, data_dictionary)
    new_pkg.generate(bbox_opt, temporal_opt)

    # checking output
    check_schema(new_pkg.data_package)
    check_fields(new_pkg.data_package)

    return new_pkg


class AedgOemetadata:
    """Makes an OEMetadata formatted metadata records and adds AEDG information to it."""

    def __init__(
        self,
        data_path: str | Path,
        sources_dir_path: str | Path,
        ddict: str,
    ) -> None:
        """Kick off the process by importing the template and config files"""

        # the template is nested dictionaries so requires deepcopy
        # see https://docs.python.org/3/library/copy.html for a clear explanation
        self.data_package = deepcopy(OEMETADATA_LATEST_TEMPLATE)
        registry_dir = Path.cwd() / "registry"

        # Read YAML config file
        # Assumed to be located right next to data and share the same name
        data_stem = Path(data_path).stem
        data_dir = Path(data_path).parents[0]

        with (data_dir / f"{data_stem}.yml").open() as stream:
            self.config = yaml.safe_load(stream)
        self.tag = data_stem
        filename = self.config["resource"]["path"].split('/')[-1]

        # Read CSV registry of fields - which might have unique definitions for this file
        if not ddict:
            self.fields = pd.read_csv(registry_dir / "fields.csv")
        else:
            self.fields = pd.read_csv(registry_dir / ddict)
        # start with fields unique to this file
        fields = self.fields.loc[self.fields['file'] == filename]
        # append all the default definitions
        fields = pd.concat(
            [fields, self.fields.loc[self.fields['file'] == 'default']],
            ignore_index=True)
        # drop the default fields if they are overridden
        self.fields = fields.drop_duplicates(subset=['name'], keep='first', ignore_index=True)

        # Read YAML registry files
        with (registry_dir / "licenses.yml").open() as stream:
            self.licenses = yaml.safe_load(stream)
        with (registry_dir / "agents.yml").open() as stream:
            self.agents = yaml.safe_load(stream)

        # Define the directory root where data source YAML files are stored
        # self.data_source = registry_dir / "data-sources"  # for testing
        # Refer to the ETL pipeline configuration files
        self.data_source = Path(sources_dir_path)


        self.output_file = data_dir / f"{data_stem}.json"



    def prep_aedg(self) -> None:
        """Make some basic changes that will be true of all AEDG metadata"""

        # Set OEMetadata context and data-pond URL
        self.data_package["@context"] ="https://raw.githubusercontent.com/OpenEnergyPlatform/oemetadata/production/oemetadata/latest/context.json"
        self.data_package["@id"] ="https://github.com/acep-aedg/aedg-data-pond"

        resource = self.data_package["resources"][0]

        resource["@id"] = self.config["resource"]["path"]

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
        resource["publicationDate"] = f"{date.today():%Y}"
        # we aren't using the OEMetadata review system
        resource.pop("review", None)
        # CSV files will always be comma delimited
        resource["dialect"]["delimiter"] = ","
        # We use "." in our floating point numbers
        resource["dialect"]["decimalSeparator"] = "."
        # Context is AEDG, but publisher is used in dataset citation and could be ISER or ACEP
        # so set that later
        resource["context"] = {
            "title": "Alaska Energy Data Gateway v3.0",
            "homepage": "https://akenergygateway.alaska.edu/",
            "publisher": None,
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
        self.data_package["description"] = self.config["resource"]["summary"]  # shorter

        # there is only 1 resource and it is same as the package
        resource = self.data_package["resources"][0]
        resource["name"] = self.config["resource"]["name"]
        resource["title"] = self.config["resource"]["title"]
        resource["description"] = self.config["resource"]["description"]

        # add keywords
        resource["keywords"] = self.config["resource"]["keywords"]
        resource["topics"] = self.config["resource"]["topics"]

        # Context is AEDG, but publisher is used in dataset citation and could be ISER or ACEP
        publisher = self.config["resource"]['publisher']
        resource["context"]["publisher"] = self.agents[publisher]['name']

        # add info about the file being described
        file_path = self.config["resource"]["path"]
        resource["path"] = file_path
        if file_path.endswith(".csv"):
            resource["type"] = "table"
            resource["format"] = "csv"
        if file_path.endswith(".geojson"):  # I don't know if OEMetadata does this
            resource["type"] = "geospatial"
            resource["format"] = "geojson"

        # check that file name is consistent with data package name and
        assert file_path.split('/')[-1].split('.')[0] == self.config["resource"]["name"]
        assert self.tag == self.config["resource"]["name"]  # from CLI call

        self.data_package["resources"][0] = resource

    def add_license(self) -> None:
        """Add the license"""

        all_licenses = []
        for license_tag in self.config["resource"]["licenses"]:
            if license_tag:
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

        # the registry fields csv with each fields a row
        con_fields = parse_combined_header(self.data_package)
        attributes = ['name', 'long_name', 'description', 'type', 'nullable', 'unit']
        assert set(attributes).issubset(set(self.fields.columns))

        fields = []
        for target in con_fields:
            row = self.fields.loc[self.fields['name'] == target, attributes].squeeze(axis=0)
            # if the field isn't found, all attributes are empty dictionaries! Blow up as warning.
            try:
                assert type(row['name']) is str
                fields.append(json.loads(row.to_json(None)))
            except AssertionError as e:
                msg = f'Field "{target}" is not in the field registry'
                raise KeyError(msg) from e

        assert len(fields) > 0
        self.data_package["resources"][0]["schema"]["fields"] = fields

        # add the primary keys from the config file - if they are described already
        primaryKeys = self.config["resource"]["primaryKey"]
        assert set(primaryKeys).issubset(set(con_fields))
        self.data_package["resources"][0]["schema"]["primaryKey"] = primaryKeys

    def add_bbox(self, bbopt: ExtentTypes) -> None:
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
            resource["spatial"]["extent"]["boundingBox"] = [-187.55, 51.21, -130.0, 71.35]
            resource["spatial"]["extent"]["crs"] = "OGC:CRS84"

        self.data_package["resources"][0] = resource

    def add_temporal(self, topt: ExtentTypes) -> None:
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
            if self.config["resource"]["temporal"]["timeseries"]:
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

    def add_sources(self) -> None:
        """Fill in documentation of the original sources define either locally or in the ETL pipeline."""

        # First test to see if any sources are defined. There might not be any.
        try:
            source_tags = self.config["resource"]["sources"]
        except KeyError:
            # there are no sources
            self.data_package["resources"][0].pop('sources', None)
            return

        # Then go through each source and transfer info in data package.
        all_sources = []
        for source_tag in source_tags:
            if type(source_tag) is dict:
                # a locally defined source, but it must be configured like the ones in the ETL pipeline
                # meaning that the key of the dictionary must be "metadata"
                assert "metadata" in source_tag
                source = source_tag
            else:
                with (self.data_source / source_tag / "source.yml").open() as stream:
                    source = yaml.safe_load(stream)
            all_licenses = []
            for license_tag in source['metadata']["sourceLicenses"]:
                if license_tag:
                    license = {"name": license_tag}
                    license.update(self.licenses["licenses"][license_tag])
                    all_licenses.append(license)
            source['metadata']["sourceLicenses"] = all_licenses

            all_sources.append(source['metadata'])

        self.data_package["resources"][0]["sources"] = all_sources

    def add_contributors(self) -> None:
        """Fill in various fields based on the values in the agents registry."""

        all_contribs = []
        for contributor in self.config["resource"]["contributors"]:
            if contributor['date'] == "now":
                contributor['date'] =  f"{date.today():%Y}"
            else:
                contributor['date'] =  str(contributor['date'])
            contributor["path"] = self.agents[contributor["organization"]]['homepage']
            contributor["organization"] = self.agents[contributor["organization"]]['name']
            all_contribs.append(contributor)

        metadata_note = {
            'organization': self.agents['acep']['name'],
            'roles': ["DataCurator"],
            'date': f"{date.today():%Y}",
            'object': "metadata via https://github.com/acep-aedg/aedg-metadata",
            'comment': "Documented sources and defined the data dictionary using OEMetadata (Frictionless) formatted metadata https://doi.org/10.5281/zenodo.15019561.\n",
            'path': self.agents['acep']['homepage'],
        }
        all_contribs.append(metadata_note)

        self.data_package["resources"][0]["contributors"] = all_contribs

    def generate(self, bbopt: ExtentTypes, topt: ExtentTypes) -> None:
        """Run all the steps"""
        self.prep_aedg()
        self.apply_config()
        self.add_license()
        self.add_fields()
        self.add_bbox(bbopt)
        self.add_temporal(topt)
        self.add_sources()
        self.add_contributors()


if __name__ == "__main__":

    pass
