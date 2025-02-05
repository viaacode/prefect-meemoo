# Pagination

[Prefect-meemoo Index](../../README.md#prefect-meemoo-index) / [Prefect Meemoo](../index.md#prefect-meemoo) / [Triplydb](./index.md#triplydb) / Pagination

> Auto-generated documentation for [prefect_meemoo.triplydb.pagination](../../../prefect_meemoo/triplydb/pagination.py) module.

- [Pagination](#pagination)
  - [_run_query](#_run_query)
  - [add_params_to_uri](#add_params_to_uri)
  - [get_triply_headers](#get_triply_headers)
  - [request_triply_get](#request_triply_get)
  - [request_triply_post](#request_triply_post)
  - [run_saved_query](#run_saved_query)
  - [run_sparql_select](#run_sparql_select)

## _run_query

[Show source in pagination.py:108](../../../prefect_meemoo/triplydb/pagination.py#L108)

Common logic for the [run_saved_query](#run_saved_query) and `run_sparql` functions

#### Signature

```python
def _run_query(send_request_fn: Callable[[int], Response]) -> Iterable: ...
```



## add_params_to_uri

[Show source in pagination.py:202](../../../prefect_meemoo/triplydb/pagination.py#L202)

#### Signature

```python
def add_params_to_uri(uri: str, params: dict[str, Any]) -> str: ...
```



## get_triply_headers

[Show source in pagination.py:192](../../../prefect_meemoo/triplydb/pagination.py#L192)

#### Signature

```python
def get_triply_headers(
    bearer_token: str, extra_headers: Union[dict[str, str], None] = None
) -> dict[str, str]: ...
```



## request_triply_get

[Show source in pagination.py:144](../../../prefect_meemoo/triplydb/pagination.py#L144)

Send a GET request including the triply token to the given endpoint.

#### Signature

```python
@task
def request_triply_get(endpoint: str, triplydb_block_name: str) -> Response: ...
```



## request_triply_post

[Show source in pagination.py:165](../../../prefect_meemoo/triplydb/pagination.py#L165)

Send a POST request including the triply token to the given endpoint.

#### Signature

```python
@task()
def request_triply_post(
    endpoint: str, body: str, triplydb_block_name: str
) -> Response: ...
```



## run_saved_query

[Show source in pagination.py:15](../../../prefect_meemoo/triplydb/pagination.py#L15)

Execute a saved query.

Unlike a simple GET request to a saved query endpoint, this function takes care of pagination. Requires prefect.
Results are yielded back as an Iterable. This means that only part of the results are kept in memory at any given time.

```py
results = run_saved_query(...)
for r in results:
    ...
```

One caveat with the `offset` parameter is that all results up to #`offset + limit` are fetched from the triple store,
including the first #`offset` results which are discarded afterwards.

Use a negative `limit` to fetch all results.

#### Signature

```python
@flow(name="Run a Triply saved query with pagination")
def run_saved_query(
    saved_query_uri: str, triplydb_block_name: str, limit: int = 10000, offset: int = 0
) -> Iterable: ...
```



## run_sparql_select

[Show source in pagination.py:56](../../../prefect_meemoo/triplydb/pagination.py#L56)

Execute a sparql SELECT query using the given endpoint.

Unlike a simple POST request to a tripple store, this function takes care of pagination. Requires prefect.
Results are yielded back as an Iterable. This means that only part of the results are kept in memory at any given time.

```py
results = run_sparql_select(...)
for r in results:
    ...
```

One caveat with the `offset` parameter is that all results up to #`offset + limit` are fetched from the triple store,
including the first #`offset` results which are discarded afterwards.

Use a negative `limit` to fetch all results.

#### Signature

```python
@flow(name="Run a sparql SELECT with pagination")
def run_sparql_select(
    endpoint: str,
    sparql: str,
    triplydb_block_name: str,
    limit: int = 10000,
    offset: int = 0,
) -> Iterable: ...
```