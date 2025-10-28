import os
from importlib.metadata import version
from typing import Optional

from prefect.blocks.core import Block, SecretStr
from pydantic import Field



class APICredentials(Block):
    """
    Block used to manage authentication with an API.

    Attributes:
        url: API URL
        authentication_url: optional API authentication URL
        username: optional API username
        password: optional API password

    Example:
        Load stored API credentials:
        ```python
        from prefect_meemoo.credentials import APICredentials
        credentials = APICredentials.load("BLOCK_NAME")
        ```
    """

    _block_type_name = "API credentials"

    url: str = Field(default=(...), description="API URL.")
    authentication_url: Optional[str] = Field(default=(...), description="API authentication URL, if applicable.")
    username: Optional[str] = Field(default=(...), description="API username, if applicable.")
    password: Optional[SecretStr] = Field(default=(...), description="API password, if applicable.")

    try:
        _block_schema_capabilities = ["meemoo-prefect", "credentials", os.environ["BUILD_CONFIG_NAME"]]
    except KeyError:
        _block_schema_capabilities = ["meemoo-prefect", "credentials", "v"+ version('prefect-meemoo')]
