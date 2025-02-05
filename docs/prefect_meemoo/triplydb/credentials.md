# Credentials

[Prefect-meemoo Index](../../README.md#prefect-meemoo-index) / [Prefect Meemoo](../index.md#prefect-meemoo) / [Triplydb](./index.md#triplydb) / Credentials

> Auto-generated documentation for [prefect_meemoo.triplydb.credentials](../../../prefect_meemoo/triplydb/credentials.py) module.

- [Credentials](#credentials)
  - [TriplyDBCredentials](#triplydbcredentials)

## TriplyDBCredentials

[Show source in credentials.py:8](../../../prefect_meemoo/triplydb/credentials.py#L8)

Block used to manage authentication with TriplyDB.

#### Attributes

- `token` - The JWT token of the user
- `owner` - The user or organization that owns the dataset
- `dataset` - "Name of the default dataset.
- `graph` - Name of the default Named Graph in the dataset.
- `host` - TriplyDB HTTP host address

#### Examples

Load stored TriplyDB credentials:

```python
from prefect_meemoo.credentials import TriplyDBCredentials
credentials = TriplyDBCredentials.load("BLOCK_NAME")
```

#### Signature

```python
class TriplyDBCredentials(Block): ...
```