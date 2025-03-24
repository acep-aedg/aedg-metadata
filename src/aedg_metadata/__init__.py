"""
Copyright (c) 2025 Elizabeth Dobbins. All rights reserved.

aedg-metadata: A CLI to generate metadata from input configuration files
in support of the Alaska Energy Data Gateway (AEDG)
"""
from __future__ import annotations

from .gen_meta import AedgOemetadata, check_schema, run_generate

__all__ = ['AedgOemetadata', 'check_schema', 'run_generate']
