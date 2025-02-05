# Credentials

[Prefect-meemoo Index](../../README.md#prefect-meemoo-index) / [Prefect Meemoo](../index.md#prefect-meemoo) / [Elasticsearch](./index.md#elasticsearch) / Credentials

> Auto-generated documentation for [prefect_meemoo.elasticsearch.credentials](../../../prefect_meemoo/elasticsearch/credentials.py) module.

- [Credentials](#credentials)
  - [ElasticsearchCredentials](#elasticsearchcredentials)
    - [ElasticsearchCredentials().get_client](#elasticsearchcredentials()get_client)

## ElasticsearchCredentials

[Show source in credentials.py:10](../../../prefect_meemoo/elasticsearch/credentials.py#L10)

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
class ElasticsearchCredentials(Block): ...
```

### ElasticsearchCredentials().get_client

[Show source in credentials.py:38](../../../prefect_meemoo/elasticsearch/credentials.py#L38)

Helper method to get an Elasticsearch client.

#### Returns

- An authenticated Elasticsearch client

#### Signature

```python
def get_client(self) -> Elasticsearch: ...
```