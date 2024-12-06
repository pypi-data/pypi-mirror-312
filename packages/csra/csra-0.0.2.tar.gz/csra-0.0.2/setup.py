from setuptools import setup
from pathlib import Path

MODULE_NAME = "sra_collector"
README_CONTENT = (Path(__file__).parent / "README.md").read_text()

setup(name="csra",
      version="0.0.2",
      description="Collect NIH NCBI SRA metadata of several GEO studies in one search.",
      packages=[MODULE_NAME],
      long_description=README_CONTENT,
      long_description_content_type="text/markdown",
      entry_points={"console_scripts": [f"csra={MODULE_NAME}.cli:main", ]}
)
