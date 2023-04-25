from prefect.blocks.core import Block
from pydantic import Field, SecretStr


class PostgresCredentials(Block):
    """
    Block used to manage authentication with Postgres.

    Attributes:
        password: Postgres password
        username: Postgres username
        host: Postgres host
        port: Postgres port

    Example:
        Load stored Postgres credentials:
        ```python
        from prefect_meemoo.credentials import PostgresCredentials
        credentials = PostgresCredentials.load("BLOCK_NAME")
        ```
    """

    _block_type_name = "Postgres Credentials"
    _logo_url = "https://www.postgresql.org/media/img/about/press/elephant.png"

    password: SecretStr = Field(default="", description="Postgres password.")
    username: str = Field(default=(...), description="Postgres username.")
    host: str = Field(default=(...), description="Postgres URL.")
    port: int = Field(default=(...), description="Postgres port.")
    database: str = Field(default=(...), description="Postgres database.")

    _block_schema_capabilities = ["meemoo-prefect", "credentials"]

