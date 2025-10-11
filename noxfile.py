import nox

prj_options = nox.project.load_toml("pyproject.toml")


@nox.session(
    python=nox.project.python_versions(prj_options, max_version="3.14")
)
def test(session):
    session.install(".")
    session.install(*nox.project.dependency_groups(prj_options, "dev"))
    session.install(*prj_options["project"]["dependencies"])
    #    session.install("cython")
    #    session.install("lxml")
    #    session.install("pytest-asyncio")
    #    session.install("pytest-cov")
    #    session.install("pytest-sugar")
    #    session.install("pytest")
    #    session.install("requests")
    #    session.install("typing-extensions")
    session.run("pytest", "tests/")
