# Credentials

[Prefect-meemoo Index](../README.md#prefect-meemoo-index) /
[Prefect Meemoo](./index.md#prefect-meemoo) /
Credentials

> Auto-generated documentation for [prefect_meemoo.credentials](../../prefect_meemoo/credentials.py) module.

- [Credentials](#credentials)
  - [PostgresCredentials](#postgrescredentials)

## PostgresCredentials

[Show source in credentials.py:5](../../prefect_meemoo/credentials.py#L5)

Block used to manage authentication with Postgres.

#### Attributes

- `password` - Postgres password
- `username` - Postgres username
- `host` - Postgres host
- `port` - Postgres port

#### Examples

Load stored Postgres credentials:

```python
from prefect_meemoo.credentials import PostgresCredentials
credentials = PostgresCredentials.load("BLOCK_NAME")
```

#### Signature

```python
class PostgresCredentials(Block):
    ...
```