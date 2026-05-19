import os
from importlib.metadata import version

from prefect.blocks.core import Block
from pydantic import Field, HttpUrl


def get_meemoo_prefect_version() -> str:
    try:
        return os.environ["BUILD_CONFIG_NAME"]
    except KeyError:
        return "v" + version("prefect-meemoo")


class String(Block):
    """
    Block used to store a string value.

    Attributes:
        value: A string value.

    Example:
        Load a stored string value:
        ```python
        from prefect_meemoo.prefect.blocks.string import String

        string_block = String.load("BLOCK_NAME")
        ```
    """

    _block_type_name = "String"
    _logo_url = HttpUrl(
        "https://cdn.sanity.io/images/3ugk85nk/production/c262ea2c80a2c043564e8763f3370c3db5a6b3e6-48x48.png"
    )

    value: str = Field(default=(...), description="A string value.")

    _block_schema_capabilities = [
        "meemoo-prefect",
        "blocks",
        get_meemoo_prefect_version(),
    ]
