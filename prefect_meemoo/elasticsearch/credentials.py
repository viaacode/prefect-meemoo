import urllib3
from elasticsearch import Elasticsearch
from prefect.blocks.core import Block
from pydantic import Field, SecretStr


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
        """
        Helper method to get an Elasticsearch client.

        Returns:
            - An authenticated Elasticsearch client
        """
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        client = Elasticsearch(
            self.url,
            basic_auth=(self.username, self.password.get_secret_value()),
            verify_certs=False,
        )
        return client