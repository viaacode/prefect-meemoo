# Tasks

[Prefect-meemoo Index](../../README.md#prefect-meemoo-index) /
[Prefect Meemoo](../index.md#prefect-meemoo) /
[Mediahaven](./index.md#mediahaven) /
Tasks

> Auto-generated documentation for [prefect_meemoo.mediahaven.tasks](../../../prefect_meemoo/mediahaven/tasks.py) module.

- [Tasks](#tasks)
  - [fragment_metadata_update](#fragment_metadata_update)
  - [generate_record_json](#generate_record_json)
  - [get_field_definition](#get_field_definition)
  - [get_organisation](#get_organisation)
  - [search_organisations](#search_organisations)
  - [search_records](#search_records)
  - [update_record](#update_record)
  - [update_single_value_flow](#update_single_value_flow)

## fragment_metadata_update

[Show source in tasks.py:254](../../../prefect_meemoo/mediahaven/tasks.py#L254)

Generate JSON for updating metadata of a fragment and update in MediaHaven.

#### Arguments

- `-` *client* - MediaHaven client
- `-` *fragment_id* - MediaHaven fragment id
- `-` *fields* - Dictionary with field's flatkey and values and optional merge strategies
    - `ex` - {"dcterms_created": {"value": "2022-01-01", "merge_strategy": "KEEP"}}

#### Returns

- True if the update was successful, False otherwise

#### Signature

```python
@task(name="Update metadata of fragment")
def fragment_metadata_update(client: MediaHaven, fragment_id: str, fields: dict) -> bool:
    ...
```



## generate_record_json

[Show source in tasks.py:166](../../../prefect_meemoo/mediahaven/tasks.py#L166)

Generate a json object that can be used to update metadata in MediaHaven

#### Arguments

- `-` *client* - MediaHaven client
- `-` *field* - Name of the field to update
- `-` *value* - Value to update the field with
- `-` *merge_strategy* - Merge strategy to use when updating the field : KEEP, OVERWRITE, MERGE or SUBTRACT (default: None)
    - `see` - [](https://mediahaven.atlassian.net/wiki/spaces/CS/pages/722567181/Metadata+Strategy)

#### Returns

- json object

#### Signature

```python
@task(name="Generate record json")
def generate_record_json(
    client: MediaHaven, field_flat_key: str, value, merge_strategy: str = None
) -> dict:
    ...
```



## get_field_definition

[Show source in tasks.py:78](../../../prefect_meemoo/mediahaven/tasks.py#L78)

Get the field definition from MediaHaven

#### Arguments

- `-` *client* - MediaHaven client
- `-` *field* - Name of the field

#### Returns

- field definition (dict)
    - Family
    - Type
    - Parent (Optional)

#### Signature

```python
@task(name="Get field definition")
def get_field_definition(client: MediaHaven, field_flat_key: str) -> dict:
    ...
```



## get_organisation

[Show source in tasks.py:22](../../../prefect_meemoo/mediahaven/tasks.py#L22)

Get an organisation from MediaHaven

#### Arguments

- `-` *client* - MediaHaven client
- `-` *organisation_id* - ID of the organisation

#### Returns

- organisation (dict)
    - ID
    - Name
    - LongName
    - ExternalID
    - CustomProperties
    - TenantGroup

#### Signature

```python
@task(name="Get organisation")
def get_organisation(client: MediaHaven, organisation_id: str) -> dict:
    ...
```



## search_organisations

[Show source in tasks.py:49](../../../prefect_meemoo/mediahaven/tasks.py#L49)

Get a list of organisations from MediaHaven

#### Arguments

- `-` *client* - MediaHaven client

#### Returns

- List of all organisations in MediaHaven (list of dicts)
    - ID
    - Name
    - LongName
    - ExternalID
    - CustomProperties
    - TenantGroup

#### Signature

```python
@task(name="Search organisations")
def search_organisations(client: MediaHaven, **query_params) -> List[dict]:
    ...
```



## search_records

[Show source in tasks.py:130](../../../prefect_meemoo/mediahaven/tasks.py#L130)

Task to query MediaHaven with a given query.

#### Arguments

- client (MediaHaven): MediaHaven client
- query (str): Query to execute
- last_modified_date (str): Last Updated data to filter on
- start_index (int): Start index of the query
- nr_of_results (int): Number of results to return

#### Returns

- `-` *dict* - Dictionary containing the results of the query

#### Signature

```python
@task(
    name="Search mediahaven records",
    cache_result_in_memory=False,
    persist_result=True,
    result_storage=LocalFileSystem(basepath="/tmp"),
)
def search_records(
    client: MediaHaven,
    query: str,
    last_modified_date=None,
    start_index=0,
    nr_of_results=100,
) -> dict:
    ...
```



## update_record

[Show source in tasks.py:105](../../../prefect_meemoo/mediahaven/tasks.py#L105)

Update metadata of a fragment.

#### Arguments

- `-` *client* - MediaHaven client
- `-` *fragment_id* - ID of the fragment to update
- `-` *xml* - XML metadata to update
- `-` *json* - JSON metadata to update

#### Returns

- True if the metadata was updated, False otherwise

#### Signature

```python
@task(name="Update record")
def update_record(client: MediaHaven, fragment_id, xml=None, json=None) -> bool:
    ...
```



## update_single_value_flow

[Show source in tasks.py:283](../../../prefect_meemoo/mediahaven/tasks.py#L283)

Flow to update metadata in MediaHaven.

#### Arguments

- `-` *fragment_id* - ID of the record to update
- `-` *field_flat_key* - FlatKey of the field to update
- `-` *value* - Value of the field to update

Blocks:
    - MediahavenCredentials:
        - `-` *client_secret* - Mediahaven API client secret
        - `-` *password* - Mediahaven API password
        - `-` *client_id* - Mediahaven API client ID
        - `-` *username* - Mediahaven API username
        - `-` *url* - Mediahaven API URL

#### Signature

```python
@flow(name="new name")
def update_single_value_flow(fragment_id: str, field_flat_key: str, value):
    ...
```