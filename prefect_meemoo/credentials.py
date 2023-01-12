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
        from prefect_meemoo import MediahavenCredentials
        credentials = MediahavenCredentials.load("BLOCK_NAME")
        ```
    """

    _block_type_name = "Mediahaven Credentials"
    _logo_url = "https://media-exp1.licdn.com/dms/image/C560BAQElh8QzdoFlRg/company-logo_200_200/0/1565769647771?e=2159024400&v=beta&t=Rz_fvyfhsfXIWNMt7NxQkEqsdrjge0jQHeZ1NPXK6IM"

    client_secret: SecretStr = Field(
        default="", description="Mediahaven API client secret."
    )
    password: SecretStr = Field(default="", description="Mediahaven API password.")
    client_id: str = Field(default="", description="Mediahaven API client ID.")
    username: str = Field(default="", description="Mediahaven API username.")
    url: str = Field(default="", description="Mediahaven API URL.")

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
