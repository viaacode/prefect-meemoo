from prefect.blocks.core import Block
from pydantic import Field, SecretStr


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
    owner: str = Field(
        default=(...), description="The user or organization that owns the dataset."
    )
    graph: str = Field(
        default=(...), description="Name of the default Named Graph in the dataset."
    )
    host: str = Field(default=(...), description="TriplyDB HTTP host address.")
    gitlab_token: SecretStr = Field(default="", description="Gitlab token.")
    _block_schema_capabilities = ["meemoo-prefect", "credentials"]