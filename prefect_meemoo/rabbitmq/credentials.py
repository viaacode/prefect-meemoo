from prefect.blocks.core import Block, SecretStr
from pydantic import Field


class RabbitMQCredentials(Block):
    """
    Block used to manage authentication with RabbitMQ.

    Attributes:
        user: RabbitMQ user
        password: RabbitMQ password
        queue: RabbitMQ queue
        exchange: RabbitMQ exchange
        host:  RabbitMQ host
        port:  RabbitMQ port

    Example:
        Load stored RabbitMQ credentials:
        ```python
        from prefect_meemoo.credentials import RabbitMQCredentials
        credentials = RabbitMQCredentials.load("BLOCK_NAME")
        ```
    """

    _block_type_name = "RabbitMQ Credentials"
    _logo_url = "https://www.rabbitmq.com/img/rabbitmq-logo-with-name.svg"

    user: SecretStr = Field(default=(...), description="RabbitMQ user")
    password: SecretStr = Field(default=(...), description="RabbitMQ password.")
    queue: str = Field(default=(...), description="RabbitMQ queue")
    exchange: str = Field(default=(...), description="RabbitMQ exchange")
    host: str = Field(default=(...), description="RabbitMQ host")
    port: str = Field(default=(...), description="RabbitMQ port")

    _block_schema_capabilities = ["meemoo-prefect", "credentials"]
