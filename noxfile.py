import nox

nox.options.default_venv_backend = "uv|virtualenv"

@nox.session
def tests(session: nox.Session) -> None:
    """
    Run the unit and regular tests.
    """
    session.install(".[test]")
    session.run("pytest", *session.posargs)

