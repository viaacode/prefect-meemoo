import os
from importlib.metadata import version

from prefect.blocks.core import Block, SecretStr
from pydantic import Field


class TriplyDBCredentials(Block):
    """
    Block used to manage authentication with TriplyDB.

    Attributes:
        token: The JWT token of the user
        owner: The user or organization that owns the dataset
        dataset: "Name of the default dataset.
        graph: Name of the default Named Graph in the dataset.
        host: TriplyDB HTTP host address

    Example:
        Load stored TriplyDB credentials:
        ```python
        from prefect_meemoo.credentials import TriplyDBCredentials
        credentials = TriplyDBCredentials.load("BLOCK_NAME")
        ```
    """

    _block_type_name = "TriplyDB Credentials"
    _logo_url = "https://triplydb.com/imgs/logos/logo-lg.svg"

    token: SecretStr = Field(default="", description="The JWT token of the user.")

    host: str = Field(default=(...), description="TriplyDB HTTP host address.")
    gitlab_token: SecretStr = Field(default="", description="Gitlab token.")
    try:
        _block_schema_capabilities = ["meemoo-prefect", "credentials", os.environ["BUILD_CONFIG_NAME"]]
    except KeyError:
        _block_schema_capabilities = ["meemoo-prefect", "credentials", "v"+ version('prefect-meemoo')]