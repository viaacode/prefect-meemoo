import sys

from setuptools import find_packages, setup

version = None
if "--new-version" in sys.argv:
    version_index = sys.argv.index("--new-version")
    version = sys.argv[version_index + 1]
    del sys.argv[version_index : version_index + 2]


with open("requirements.txt") as install_requires_file:
    install_requires = install_requires_file.read().strip().split("\n")

with open("requirements-dev.txt") as dev_requires_file:
    dev_requires = dev_requires_file.read().strip().split("\n")

with open("requirements-rdf.txt") as rdf_requires_file:
    rdf_requires = rdf_requires_file.read().strip().split("\n")

with open("requirements-mediahaven.txt") as mediahaven_requires_file:
    mediahaven_requires = mediahaven_requires_file.read().strip().split("\n")

with open("requirements-elasticsearch.txt") as elasticsearch_requires_file:
    elasticsearch_requires = elasticsearch_requires_file.read().strip().split("\n")

with open("requirements-triplydb.txt") as triplydb_requires_file:
    triplydb_requires = triplydb_requires_file.read().strip().split("\n")

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    name="prefect-meemoo",
    version=version,
    description="Meemoo Prefect collection with common tasks",
    license="Apache License 2.0",
    author="Lennert Van de Velde",
    author_email="lennert.vandevelde@meemoo.be",
    keywords="prefect",
    url="https://github.com/viaacode/prefect-meemoo",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests", "docs")),
    python_requires=">=3.7",
    install_requires=install_requires,
    extras_require={
        "dev": dev_requires,
        "rdf": rdf_requires,
        "mediahaven": mediahaven_requires,
        "elasticsearch": elasticsearch_requires,
        "triplydb": triplydb_requires,
    },
)

