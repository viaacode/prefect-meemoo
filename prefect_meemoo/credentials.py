import urllib3
from elasticsearch import Elasticsearch
from mediahaven import MediaHaven
from mediahaven.oauth2 import ROPCGrant
from prefect.blocks.core import Block
from pydantic import Field, SecretStr


class MediahavenCredentials(Block):
    """
    Block used to manage authentication with Mediahaven.

    Attributes:
        client_secret: Mediahaven API client secret
        password: Mediahaven API password
        client_id: Mediahaven API client ID
        username: Mediahaven API username
        url:  Mediahaven API URL

    Example:
        Load stored Mediahaven credentials:
        ```python
        from prefect_meemoo.credentials import MediahavenCredentials
        credentials = MediahavenCredentials.load("BLOCK_NAME")
        ```
    """

    _block_type_name = "Mediahaven Credentials"
    _logo_url = "https://media-exp1.licdn.com/dms/image/C560BAQElh8QzdoFlRg/company-logo_200_200/0/1565769647771?e=2159024400&v=beta&t=Rz_fvyfhsfXIWNMt7NxQkEqsdrjge0jQHeZ1NPXK6IM"

    client_secret: SecretStr = Field(
        default=(...), description="Mediahaven API client secret."
    )
    password: SecretStr = Field(default=(...), description="Mediahaven API password.")
    client_id: str = Field(default=(...), description="Mediahaven API client ID.")
    username: str = Field(default=(...), description="Mediahaven API username.")
    url: str = Field(default=(...), description="Mediahaven API URL.")

    _block_schema_capabilities = ["meemoo-prefect", "credentials"]
    
    def get_client(self) -> MediaHaven:
        '''
        Helper method to get a MediaHaven client.

        Returns:
            - An authenticated MediaHaven client

        Raises:
            - ValueError: if the authentication failed.
            - RequestTokenError: is the token cannot be requested
        '''

        grant = ROPCGrant(self.url, self.client_id, self.client_secret.get_secret_value())
        grant.request_token(self.username, self.password.get_secret_value())
        # Create MediaHaven client
        client = MediaHaven(self.url, grant)
        return client


class ElasticsearchCredentials(Block):
    """
    Block used to manage authentication with Elasticsearch.

    Attributes:
        password: Elasticsearch password
        username: Elasticsearch username
        url: Elasticsearch URL

    Example:
        Load stored Elasticsearch credentials:
        ```python
        from prefect_meemoo.credentials import ElasticsearchCredentials
        credentials = ElasticsearchCredentials.load("BLOCK_NAME")
        ```
    """

    _block_type_name = "Elasticsearch Credentials"
    _logo_url = "https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blt5d10f3a91df97d15/620a9ac8849cd422f315b83d/logo-elastic-vertical-reverse.svg"

    password: SecretStr = Field(default=(...), description="Elasticsearch password.")
    username: str = Field(default=(...), description="Elasticsearch username.")
    url: str = Field(default=(...), description="Elasticsearch URL.")
    
    _block_schema_capabilities = ["meemoo-prefect", "credentials"]

    def get_client(self) -> Elasticsearch:
        '''
        Helper method to get an Elasticsearch client.

        Returns:
            - An authenticated Elasticsearch client
        '''
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        client = Elasticsearch(
            self.url,
            basic_auth=(self.username, self.password.get_secret_value()),
            verify_certs=False,
        )
        return client

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

    password: SecretStr = Field(default ="", description="Postgres password.")
    username: str = Field(default=(...), description="Postgres username.")
    host: str = Field(default=(...), description="Postgres URL.")
    port: int = Field(default=(...), description="Postgres port.")

    _block_schema_capabilities = ["meemoo-prefect", "credentials"]

