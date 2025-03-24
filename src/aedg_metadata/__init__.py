"""
Copyright (c) 2025 Elizabeth Dobbins. All rights reserved.

aedg-metadata: A CLI to generate metadata from input configuration files
in support of the Alaska Energy Data Gateway (AEDG)
"""
from __future__ import annotations

from enum import Enum


class ExtentTypes(str, Enum):
    """Different ways to make spatial and temporal extents.
    Annotations failed syntax checks, or they would look like:
    infer: Annotated[str, "Infer the extent from the file qualities."] = "infer"
    calc: Annotated[str, "Calculate the extent from values in the file."] = "calc"
    specify: Annotated[str, "Read the extent from values in the config file."] = "specify"
    none: Annotated[str, "Do not include extent."] = "none"
    """
    infer = 'infer'
    calc = 'calc'
    specify = 'specify'
    none = 'none'
