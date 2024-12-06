from setuptools import setup
import re
from pathlib import Path

MODULE_NAME = "sra_collector"
README_CONTENT = (Path(__file__).parent / "README.md").read_text()


def get_version():
    version_file = Path(__file__).parent / MODULE_NAME / "__init__.py"
    with open(version_file, "r") as f:
        content = f.read()
        version_match = re.search(r'^__version__\s*=\s*["\']([^"\']+)["\']', content, re.M)
        if version_match:
            return version_match.group(1)
        raise RuntimeError("Unable to find version string.")


setup(name="csra",
      version=get_version(),
      packages=[MODULE_NAME],
      long_description=README_CONTENT,
      long_description_content_type="text/markdown",
      entry_points={"console_scripts": [f"csra={MODULE_NAME}.cli:main", ]}
      )
