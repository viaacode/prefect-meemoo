# Credentials

[Prefect-meemoo Index](../../README.md#prefect-meemoo-index) / [Prefect Meemoo](../index.md#prefect-meemoo) / [Rabbitmq](./index.md#rabbitmq) / Credentials

> Auto-generated documentation for [prefect_meemoo.rabbitmq.credentials](../../../prefect_meemoo/rabbitmq/credentials.py) module.

- [Credentials](#credentials)
  - [RabbitMQCredentials](#rabbitmqcredentials)

## RabbitMQCredentials

[Show source in credentials.py:5](../../../prefect_meemoo/rabbitmq/credentials.py#L5)

Block used to manage authentication with RabbitMQ.

#### Attributes

- `user` - RabbitMQ user
- `password` - RabbitMQ password
- `queue` - RabbitMQ queue
- `exchange` - RabbitMQ exchange
- `host` - RabbitMQ host
- `port` - RabbitMQ port

#### Examples

Load stored RabbitMQ credentials:

```python
from prefect_meemoo.credentials import RabbitMQCredentials
credentials = RabbitMQCredentials.load("BLOCK_NAME")
```

#### Signature

```python
class RabbitMQCredentials(Block): ...
```