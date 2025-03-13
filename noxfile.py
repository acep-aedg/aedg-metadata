import nox

nox.options.default_venv_backend = "uv|virtualenv"

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
    session.run("pytest", external=True, *session.posargs)

