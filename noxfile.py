from __future__ import annotations

import nox

nox.needs_version = ">=2024.3.2"
nox.options.sessions = ["lint", "tests"]
nox.options.default_venv_backend = "uv|virtualenv"


@nox.session
def lint(session: nox.Session) -> None:
    """
    Run the linter.
    """
    session.install("pre-commit")
    session.run(
        "pre-commit", "run", "--all-files", "--show-diff-on-failure", *session.posargs
    )


@nox.session
def tests(session: nox.Session) -> None:
    """
    Run the unit and regular tests.
    Added "external" flag because of error:
     "Warning: pytest is not installed into the virtualenv,
     it is located at /Users/eldobbins/Desktop/code/aedg-metadata/.venv/bin/pytest.
     This might cause issues! Pass external=True into run() to silence this message."
    """
    session.install(".[test]")
    session.run("pytest", *session.posargs, external=True)
