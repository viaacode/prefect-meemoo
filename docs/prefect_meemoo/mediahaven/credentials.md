# Credentials

[Prefect-meemoo Index](../../README.md#prefect-meemoo-index) / [Prefect Meemoo](../index.md#prefect-meemoo) / [Mediahaven](./index.md#mediahaven) / Credentials

> Auto-generated documentation for [prefect_meemoo.mediahaven.credentials](../../../prefect_meemoo/mediahaven/credentials.py) module.

- [Credentials](#credentials)
  - [MediahavenCredentials](#mediahavencredentials)
    - [MediahavenCredentials().get_client](#mediahavencredentials()get_client)

## MediahavenCredentials

[Show source in credentials.py:10](../../../prefect_meemoo/mediahaven/credentials.py#L10)

Block used to manage authentication with Mediahaven.

#### Attributes

- `client_secret` - Mediahaven API client secret
- `password` - Mediahaven API password
- `client_id` - Mediahaven API client ID
- `username` - Mediahaven API username
- `url` - Mediahaven API URL

#### Examples

Load stored Mediahaven credentials:

```python
from prefect_meemoo.credentials import MediahavenCredentials
credentials = MediahavenCredentials.load("BLOCK_NAME")
```

#### Signature

```python
class MediahavenCredentials(Block): ...
```

### MediahavenCredentials().get_client

[Show source in credentials.py:45](../../../prefect_meemoo/mediahaven/credentials.py#L45)

Helper method to get a MediaHaven client.

#### Returns

- An authenticated MediaHaven client

#### Raises

- `-` *ValueError* - if the authentication failed.
- `-` *RequestTokenError* - is the token cannot be requested

#### Signature

```python
def get_client(self) -> MediaHaven: ...
```