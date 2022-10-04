from setuptools import find_packages, setup


with open("requirements.txt") as install_requires_file:
    install_requires = install_requires_file.read().strip().split("\n")

with open("requirements-dev.txt") as dev_requires_file:
    dev_requires = dev_requires_file.read().strip().split("\n")

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    name="prefect-meemoo",
    version="0.1.1",
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
    extras_require={"dev": dev_requires},
)
