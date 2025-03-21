"""Tests to make sure CLI is working right"""
from __future__ import annotations

import pytest
from typer.testing import CliRunner

from aedg_metadata.cli import app

runner = CliRunner()


def test_app() -> None:
    result = runner.invoke(app, ["greet", "Camila", "--count", 14])
    assert result.exit_code == 0
    lines = result.stdout.split("\n")
    assert "Hello Camila" in result.stdout
    assert len(lines) == pytest.approx(14 + 1)


def test_raises() -> None:
    result = runner.invoke(app, ["greet", "--count", 14])
    assert result.exit_code == 2
    assert "Usage" in result.stdout
    assert "Error" in result.stdout
