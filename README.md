# prefect-meemoo

<p align="center">
    <a href="https://pypi.python.org/pypi/prefect-meemoo/" alt="PyPI version">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/prefect-meemoo?color=0052FF&labelColor=090422"></a>
    <a href="https://github.com/viaacode/prefect-meemoo/" alt="Stars">
        <img src="https://img.shields.io/github/stars/viaacode/prefect-meemoo?color=0052FF&labelColor=090422" /></a>
    <a href="https://pepy.tech/badge/prefect-meemoo/" alt="Downloads">
        <img src="https://img.shields.io/pypi/dm/prefect-meemoo?color=0052FF&labelColor=090422" /></a>
    <a href="https://github.com/viaacode/prefect-meemoo/pulse" alt="Activity">
        <img src="https://img.shields.io/github/commit-activity/m/viaacode/prefect-meemoo?color=0052FF&labelColor=090422" /></a>
    <br>
    <a href="https://prefect-meemoo-community.slack.com" alt="Slack">
        <img src="https://img.shields.io/badge/slack-join_community-red.svg?color=0052FF&labelColor=090422&logo=slack" /></a>
    <a href="https://discourse.prefect-meemoo.io/" alt="Discourse">
        <img src="https://img.shields.io/badge/discourse-browse_forum-red.svg?color=0052FF&labelColor=090422&logo=discourse" /></a>
</p>

## Welcome!

Meemoo Prefect collection with common tasks

## Getting Started

### Python setup

Requires an installation of Python 3.7+.

We recommend using a Python virtual environment manager such as pipenv, conda or virtualenv.

These tasks are designed to work with Prefect 2.0. For more information about how to use Prefect, please refer to the [Prefect documentation](https://orion-docs.prefect.io/).

### Installation

Install `prefect-meemoo` with `pip`:

```bash
pip install prefect-meemoo
```

Then, register to [view the block](https://orion-docs.prefect.io/ui/blocks/) on Prefect Cloud:

```bash
prefect block register -m prefect_meemoo.credentials
```

Note, to use the `load` method on Blocks, you must already have a block document [saved through code](https://orion-docs.prefect.io/concepts/blocks/#saving-blocks) or [saved through the UI](https://orion-docs.prefect.io/ui/blocks/).

### Write and run a flow

```python
from prefect import flow
from prefect_meemoo.tasks import (
    goodbye_prefect_meemoo,
    hello_prefect_meemoo,
)


@flow
def example_flow():
    hello_prefect_meemoo
    goodbye_prefect_meemoo

example_flow()
```

## Resources

If you encounter any bugs while using `prefect-meemoo`, feel free to open an issue in the [prefect-meemoo](https://github.com/viaacode/prefect-meemoo) repository.

If you have any questions or issues while using `prefect-meemoo`, you can find help in either the [Prefect Discourse forum](https://discourse.prefect.io/) or the [Prefect Slack community](https://prefect.io/slack).

## Development

If you'd like to install a version of `prefect-meemoo` for development, clone the repository and perform an editable install with `pip`:

```bash
git clone https://github.com/viaacode/prefect-meemoo.git

cd prefect-meemoo/

pip install -e ".[dev]"

# Install linting pre-commit hooks
pre-commit install
```
