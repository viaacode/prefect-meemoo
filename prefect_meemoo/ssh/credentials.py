import os
from importlib.metadata import version

from prefect.blocks.core import Block
from pydantic import SecretStr
from pydantic import Field


class SSHCredentials(Block):
    """
    Block used to manage authentication with SSH.

    Attributes:
        password: SSH password
        user: remote SSH user
        host: remote SSH host
        post: SSH port

    Example:
        Load stored SSH credentials:
        ```python
        from prefect_meemoo.ssh import SSHCredentials
        credentials = SSHCredentials.load("BLOCK_NAME")
        ```
    """

    _block_type_name = "SSH Credentials"
    _logo_url = "https://cdn-icons-png.flaticon.com/128/10147/10147353.png"

    hostname: str = Field(default=(...), description="SSH hostname.")
    port: int = Field(default=22, description="SSH port.")
    user: str = Field(default=(...), description="SSH user.")
    password: SecretStr = Field(default=(...), description="SSH password.")

    try:
        _block_schema_capabilities = [
            "meemoo-prefect",
            "credentials",
            os.environ["BUILD_CONFIG_NAME"],
        ]
    except KeyError:
        _block_schema_capabilities = [
            "meemoo-prefect",
            "credentials",
            "v" + version("prefect-meemoo"),
        ]
