# Tasks

[Prefect-meemoo Index](../../README.md#prefect-meemoo-index) /
[Prefect Meemoo](../index.md#prefect-meemoo) /
[Rdf](./index.md#rdf) /
Tasks

> Auto-generated documentation for [prefect_meemoo.rdf.tasks](../../../prefect_meemoo/rdf/tasks.py) module.

- [Tasks](#tasks)
  - [combine_ntriples](#combine_ntriples)
  - [compare](#compare)
  - [create_sparqlwrapper](#create_sparqlwrapper)
  - [dict_to_rdf](#dict_to_rdf)
  - [json_to_rdf](#json_to_rdf)
  - [resolve_text](#resolve_text)
  - [sparql_gsp_delete](#sparql_gsp_delete)
  - [sparql_gsp_get](#sparql_gsp_get)
  - [sparql_gsp_post](#sparql_gsp_post)
  - [sparql_gsp_put](#sparql_gsp_put)
  - [sparql_select](#sparql_select)
  - [sparql_transform](#sparql_transform)
  - [sparql_transform_insert](#sparql_transform_insert)
  - [sparql_update_clear](#sparql_update_clear)
  - [sparql_update_insert](#sparql_update_insert)
  - [sparql_update_query](#sparql_update_query)
  - [to_ntriples](#to_ntriples)
  - [validate_ntriples](#validate_ntriples)

## combine_ntriples

[Show source in tasks.py:423](../../../prefect_meemoo/rdf/tasks.py#L423)

Concatenates a couple of ntriples lines

#### Returns

- `str*` - ntriple line to add

#### Signature

```python
@task(name="concatenate ntriples")
def combine_ntriples(*ntriples: str):
    ...
```



## compare

[Show source in tasks.py:301](../../../prefect_meemoo/rdf/tasks.py#L301)

#### Signature

```python
@task(name="compare RDF files")
def compare(input_data1: str, input_data2: str):
    ...
```



## create_sparqlwrapper

[Show source in tasks.py:465](../../../prefect_meemoo/rdf/tasks.py#L465)

#### Signature

```python
def create_sparqlwrapper(endpoint: str, method: str = None, auth: AuthBase = None):
    ...
```



## dict_to_rdf

[Show source in tasks.py:343](../../../prefect_meemoo/rdf/tasks.py#L343)

Converts Python dict objects to RDF by direct mapping

#### Arguments

- `input_data*` - arbitrary list of dict to map
- `ns` *str, optional* - Namespace to use to build RDF predicates. Defaults to https://data.hetarchief.be/ns/source#.

#### Returns

- `str` - ntriples serialization of the result

#### Signature

```python
@task(name="convert python dict to rdf")
def dict_to_rdf(ns: str = SRC_NS, *input_data: dict):
    ...
```

#### See also

- [SRC_NS](#src_ns)



## json_to_rdf

[Show source in tasks.py:321](../../../prefect_meemoo/rdf/tasks.py#L321)

Converts JSON documents to RDF by direct mapping

#### Arguments

- `input_data*` - arbitrary list of JSON strings to map
- `ns` *str, optional* - Namespace to use to build RDF predicates. Defaults to https://data.hetarchief.be/ns/source#.

#### Returns

- `str` - ntriples serialization of the result

#### Signature

```python
@task(name="convert json to rdf")
def json_to_rdf(ns: str = SRC_NS, *input_data: str):
    ...
```

#### See also

- [SRC_NS](#src_ns)



## resolve_text

[Show source in tasks.py:483](../../../prefect_meemoo/rdf/tasks.py#L483)

#### Signature

```python
def resolve_text(value):
    ...
```



## sparql_gsp_delete

[Show source in tasks.py:101](../../../prefect_meemoo/rdf/tasks.py#L101)

Send a DELETE request to a SPARQL Graph Store HTTP Protocol endpoint

#### Arguments

- endpoint (str): The URL of the SPARQL Graph Store endpoint
- graph (str, optional): A URI identifying the named graph to delete.
        If set to None, the `endpoint` parameter is assumed to be using
        [Direct Graph Identification](https://www.w3.org/TR/sparql11-http-rdf-update/#direct-graph-identification).
- auth (AuthBase, optional): a `requests` library authentication object

#### Returns

- True if the DELETE was successful, False otherwise

#### Signature

```python
@task(name="SPARQL Graph Store 1.1 DELETE")
def sparql_gsp_delete(
    endpoint: str, graph: str = None, auth: AuthBase = None, timeout: float = TIMEOUT
):
    ...
```

#### See also

- [TIMEOUT](#timeout)



## sparql_gsp_get

[Show source in tasks.py:130](../../../prefect_meemoo/rdf/tasks.py#L130)

Send a GET request to a SPARQL Graph Store HTTP Protocol endpoint

#### Arguments

- endpoint (str): The URL of the SPARQL Graph Store endpoint
- graph (str, optional): A URI identifying the named graph to get.
        If set to None, the `endpoint` parameter is assumed to be using
        [Direct Graph Identification](https://www.w3.org/TR/sparql11-http-rdf-update/#direct-graph-identification).
- content_type (str, optional): the deisred mimeType of the result. Defaults to "text/turtle".
- auth (AuthBase, optional): a `requests` library authentication object

#### Returns

- True if the POST was successful, False otherwise

#### Signature

```python
@task(name="SPARQL Graph Store 1.1 GET")
def sparql_gsp_get(
    endpoint: str,
    graph: str = None,
    content_type: str = "text/turtle",
    auth: AuthBase = None,
    timeout: float = TIMEOUT,
):
    ...
```

#### See also

- [TIMEOUT](#timeout)



## sparql_gsp_post

[Show source in tasks.py:25](../../../prefect_meemoo/rdf/tasks.py#L25)

Send a POST request to a SPARQL Graph Store HTTP Protocol endpoint

#### Arguments

- input_data (str): Serialized RDF data to be POSTed to the endpoint
- endpoint (str): The URL of the SPARQL Graph Store endpoint
- graph (str, optional): A URI identifying the named graph to post to.
        If set to None, the `endpoint` parameter is assumed to be using
        [Direct Graph Identification](https://www.w3.org/TR/sparql11-http-rdf-update/#direct-graph-identification).
- content_type (str, optional): the mimeType of the `input_data`. Defaults to "text/turtle".
- auth (AuthBase, optional): a `requests` library authentication object

#### Returns

- True if the POST was successful, False otherwise

#### Signature

```python
@task(name="SPARQL Graph Store 1.1 POST")
def sparql_gsp_post(
    input_data: str,
    endpoint: str,
    graph: str = None,
    content_type: str = "text/turtle",
    auth: AuthBase = None,
    timeout: float = TIMEOUT,
):
    ...
```

#### See also

- [TIMEOUT](#timeout)



## sparql_gsp_put

[Show source in tasks.py:63](../../../prefect_meemoo/rdf/tasks.py#L63)

Send a PUT request to a SPARQL Graph Store HTTP Protocol endpoint

#### Arguments

- input_data (str): Serialized RDF data to be PUT to the endpoint
- endpoint (str): The URL of the SPARQL Graph Store endpoint
- graph (str, optional): A URI identifying the named graph to put to.
        If set to None, the `endpoint` parameter is assumed to be using
        [Direct Graph Identification](https://www.w3.org/TR/sparql11-http-rdf-update/#direct-graph-identification).
- content_type (str, optional): the mimeType of the `input_data`. Defaults to "text/turtle".
- auth (AuthBase, optional): a `requests` library authentication object

#### Returns

- True if the PUT was successful, False otherwise

#### Signature

```python
@task(name="SPARQL Graph Store 1.1 PUT")
def sparql_gsp_put(
    input_data: str,
    endpoint: str,
    graph: str = None,
    content_type: str = "text/turtle",
    auth: AuthBase = None,
    timeout: float = TIMEOUT,
):
    ...
```

#### See also

- [TIMEOUT](#timeout)



## sparql_select

[Show source in tasks.py:164](../../../prefect_meemoo/rdf/tasks.py#L164)

Execute SPARQL SELECT query on a SPARQL endpoint and get the results in a pandas dataframe.

#### Arguments

- query (str): SPARQL SELECT query to execute
- endpoint (str): The URL of the SPARQL endpoint
- method (str): The HTTP method to use. Defaults to POST
- headers (dict, optional): Python dict with HTTP headers to add.
- auth (AuthBase, optional): a `requests` library authentication object

#### Returns

- Pandas DataFrame with query results

#### Signature

```python
@task(name="execute SPARQL SELECT query")
def sparql_select(
    query: str,
    endpoint: str,
    method: str = "POST",
    headers: Optional[Dict[str, Any]] = None,
    auth: AuthBase = None,
):
    ...
```



## sparql_transform

[Show source in tasks.py:365](../../../prefect_meemoo/rdf/tasks.py#L365)

Transforms one RDF graph in another using a CONSTRUCT query

#### Arguments

- `*input_data` - input RDF graph serialized as ntriples.
- `query` *str* - SPARQL construct query either as file path or as query text.

#### Returns

- `str` - result RDF graph serialized as ntriples

#### Signature

```python
@task(name="sparql transformation")
def sparql_transform(input_data: str, query: str):
    ...
```



## sparql_transform_insert

[Show source in tasks.py:395](../../../prefect_meemoo/rdf/tasks.py#L395)

Transforms one RDF graph in another using an INSERT query

#### Arguments

- `*input_data` - input RDF graph serialized as ntriples.
- `query` *str* - SPARQL construct query either as file path or as query text.
- `target_graph` *str* - graph in which the result is inserted

#### Returns

- `str` - result RDF graph serialized as ntriples

#### Signature

```python
def sparql_transform_insert(input_data: str, query: str, target_graph: str):
    ...
```



## sparql_update_clear

[Show source in tasks.py:283](../../../prefect_meemoo/rdf/tasks.py#L283)

Clear a graph using SPARQL Update.

#### Arguments

- graph (str): A URI identifying the named graph to insert the triples into.
- endpoint (str): The URL of the SPARQL endpoint
- silent (bool):

#### Returns

- True if the request was successful, False otherwise

#### Signature

```python
@task(name="clear graph")
def sparql_update_clear(graph, endpoint, silent=True):
    ...
```



## sparql_update_insert

[Show source in tasks.py:253](../../../prefect_meemoo/rdf/tasks.py#L253)

Insert an iterable of RDFLib triples using SPARQL Update.

#### Arguments

- triples (List): List of triples
- endpoint (str): The URL of the SPARQL endpoint
- graph (str, optional): A URI identifying the named graph to insert the triples into. If set to `None`, the default graph is assumed.

#### Returns

- True if the request was successful, False otherwise

#### Signature

```python
@task(name="insert RDF triples")
def sparql_update_insert(triples, endpoint, graph=None):
    ...
```



## sparql_update_query

[Show source in tasks.py:212](../../../prefect_meemoo/rdf/tasks.py#L212)

Execute SPARQL Update on a SPARQL endpoint.

#### Arguments

- query (str): SPARQL Update query to execute
- endpoint (str): The URL of the SPARQL endpoint
- method (str): The HTTP method to use. Defaults to POST
- headers (dict, optional): Python dict with HTTP headers to add.
- auth (AuthBase, optional): a `requests` library authentication object

#### Returns

- True if the request was successful, False otherwise

#### Signature

```python
@task(name="execute SPARQL Update query")
def sparql_update_query(
    query: str,
    endpoint: str,
    method: str = "POST",
    headers: Optional[Dict[str, Any]] = None,
    auth: AuthBase = None,
):
    ...
```



## to_ntriples

[Show source in tasks.py:457](../../../prefect_meemoo/rdf/tasks.py#L457)

#### Signature

```python
def to_ntriples(t, namespace_manager=None):
    ...
```



## validate_ntriples

[Show source in tasks.py:435](../../../prefect_meemoo/rdf/tasks.py#L435)

#### Signature

```python
@task(name="validate ntriples")
def validate_ntriples(input_data: str, shacl_graph: str, ont_graph: str = None):
    ...
```