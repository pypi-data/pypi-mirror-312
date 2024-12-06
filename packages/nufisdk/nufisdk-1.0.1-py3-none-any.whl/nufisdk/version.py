import toml
import os


def get_version():
    """Extract version from pyproject.toml"""
    pyproject_path = os.path.join(os.path.dirname(__file__), "../pyproject.toml")
    with open(pyproject_path, "r") as f:
        pyproject_data = toml.load(f)
    return pyproject_data["tool"]["poetry"]["version"]


__version__ = get_version()
