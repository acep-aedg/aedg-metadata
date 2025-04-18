"""Tests to make sure metadata generation is working right"""
from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from aedg_metadata import ExtentTypes
from aedg_metadata.gen_meta import run_generate


@pytest.fixture  # type: ignore[misc]
def ref_pkg() -> dict[Any, Any]:
    """Read in the reference package"""
        # load the reference file
    ref_dir = Path(__file__).parents[0]
    ref_file = ref_dir / "resources" / "public_communities_monthly_generation_reference.json"
    with ref_file.open(mode="r") as file:
        pkg = json.load(file)
    # remove dates because those won't match
    pkg["resources"][0].pop("publicationDate", None)
    pkg["resources"][0]["contributors"][0].pop("date", None)
    return pkg  # type: ignore[no-any-return]


@pytest.fixture  # type: ignore[misc]
def pkg_specified() -> dict[Any, Any]:
    config = 'public_communities_monthly_generation'
    subdirectory = '../../tests/resources'
    data_dictionary = ""
    bbox = ExtentTypes.specify
    temporal = ExtentTypes.specify
    pkg = run_generate(config, subdirectory, data_dictionary, bbox, temporal)
    pkg.data_package["resources"][0].pop("publicationDate", None)
    pkg.data_package["resources"][0]["contributors"][0].pop("date", None)
    return pkg.data_package  # type: ignore[no-any-return]


@pytest.fixture  # type: ignore[misc]
def pkg_no_bounds() -> dict[Any, Any]:
    config = 'public_communities_monthly_generation'
    subdirectory = '../../tests/resources'
    data_dictionary = ""
    bbox = ExtentTypes.none
    temporal = ExtentTypes.none
    pkg = run_generate(config, subdirectory, data_dictionary, bbox, temporal)
    pkg.data_package["resources"][0].pop("publicationDate", None)
    pkg.data_package["resources"][0]["contributors"][0].pop("date", None)
    return pkg.data_package  # type: ignore[no-any-return]


@pytest.fixture   # type: ignore[misc]
def pkg_inferred() -> dict[Any, Any]:
    config = 'public_communities_monthly_generation'
    subdirectory = '../../tests/resources'
    data_dictionary = ""
    bbox = ExtentTypes.infer
    temporal = ExtentTypes.infer
    pkg = run_generate(config, subdirectory, data_dictionary, bbox, temporal)
    pkg.data_package["resources"][0].pop("publicationDate", None)
    pkg.data_package["resources"][0]["contributors"][0].pop("date", None)
    return pkg.data_package  # type: ignore[no-any-return]


def test_stability(ref_pkg: dict[Any, Any], pkg_specified: dict[Any, Any]) -> None:
    """To make sure refactoring doesn't inadvertently change the output"""

    assert pkg_specified == ref_pkg


def test_no_spatial_temporal(ref_pkg: dict[Any, Any], pkg_no_bounds: dict[Any, Any]) -> None:
    """Test that will drop spatial and temporal if instructed to"""

    tester = deepcopy(ref_pkg)
    tester['resources'][0].pop('spatial', None)
    tester['resources'][0].pop('temporal', None)
    assert pkg_no_bounds == tester


def test_infer_spatial_temporal(ref_pkg: dict[Any, Any], pkg_inferred: dict[Any, Any]) -> None:
    """Test that will infer spatial and temporal if instructed to"""

    tester = deepcopy(ref_pkg)
    tester['resources'][0]["temporal"]['referenceDate'] = '2025-01-01'  # arbitrary
    tester['resources'][0]['temporal'].pop('timeseries', None)
    assert pkg_inferred == tester
