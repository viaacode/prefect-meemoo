# Credentials

[Prefect-meemoo Index](../README.md#prefect-meemoo-index) /
[Prefect Meemoo](./index.md#prefect-meemoo) /
Credentials

> Auto-generated documentation for [prefect_meemoo.credentials](../../prefect_meemoo/credentials.py) module.

- [Credentials](#credentials)
  - [ElasticsearchCredentials](#elasticsearchcredentials)
    - [ElasticsearchCredentials().get_client](#elasticsearchcredentials()get_client)
  - [MediahavenCredentials](#mediahavencredentials)
    - [MediahavenCredentials().get_client](#mediahavencredentials()get_client)
  - [PostgresCredentials](#postgrescredentials)
  - [TriplyDBCredentials](#triplydbcredentials)

## ElasticsearchCredentials

[Show source in credentials.py:62](../../prefect_meemoo/credentials.py#L62)

Block used to manage authentication with Elasticsearch.

#### Attributes

- `password` - Elasticsearch password
- `username` - Elasticsearch username
- `url` - Elasticsearch URL

#### Examples

Load stored Elasticsearch credentials:

```python
from prefect_meemoo.credentials import ElasticsearchCredentials
credentials = ElasticsearchCredentials.load("BLOCK_NAME")
```

#### Signature

```python
class ElasticsearchCredentials(Block):
    ...
```

### ElasticsearchCredentials().get_client

[Show source in credentials.py:88](../../prefect_meemoo/credentials.py#L88)

Helper method to get an Elasticsearch client.

#### Returns

- An authenticated Elasticsearch client

#### Signature

```python
def get_client(self) -> Elasticsearch:
    ...
```



## MediahavenCredentials

[Show source in credentials.py:9](../../prefect_meemoo/credentials.py#L9)

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
class MediahavenCredentials(Block):
    ...
```

### MediahavenCredentials().get_client

[Show source in credentials.py:41](../../prefect_meemoo/credentials.py#L41)

Helper method to get a MediaHaven client.

#### Returns

- An authenticated MediaHaven client

#### Raises

- `-` *ValueError* - if the authentication failed.
- `-` *RequestTokenError* - is the token cannot be requested

#### Signature

```python
def get_client(self) -> MediaHaven:
    ...
```



## PostgresCredentials

[Show source in credentials.py:105](../../prefect_meemoo/credentials.py#L105)

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



## TriplyDBCredentials

[Show source in credentials.py:135](../../prefect_meemoo/credentials.py#L135)

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
class TriplyDBCredentials(Block):
    ...
```