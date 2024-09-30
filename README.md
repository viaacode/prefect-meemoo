# Prefect Meemoo Task Library
## Summary

This package contains a collection of reusable Prefect tasks and blocks in the meemoo context. It consists of several subpackages that can (and should) be imported individually as such:

```
pip install prefect-meemoo[{subpackage}]
```

Documentation for each subpackage can be found in [the documentation folder.](./docs/)
## DEV Guidelines

### Package Structure
The [prefect_meemoo](./prefect_meemoo/) folder contains subfolders for each subpackage. Corresponding to these, a `requirements-{package-name}.txt` file must be added in the root folder. In [setup.py](setup.py), these requirement files must be imported and added to the `extras_require` argument of setup.

### Generating Documentation
Run the `handsdown` command in the root folder after installing the dev dependencies.

### Deployment
Releasing a tag will deploy the package on one of the Meemoo Prefect environments:
- Alpha tag (`vX.X.X-aX`) will deploy on INT.
- Beta tag (`vX.X.X-bX`) will deploy on QAS.
- Major tag (`vX.X.X`) will deploy on PRD.

Blocks that should be registered on the servers are defined in a [blocks.yaml](./.openshift/blocks.yaml).
