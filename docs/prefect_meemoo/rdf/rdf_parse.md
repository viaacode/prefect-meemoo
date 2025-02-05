# Rdf Parse

[Prefect-meemoo Index](../../README.md#prefect-meemoo-index) / [Prefect Meemoo](../index.md#prefect-meemoo) / [Rdf](./index.md#rdf) / Rdf Parse

> Auto-generated documentation for [prefect_meemoo.rdf.rdf_parse](../../../prefect_meemoo/rdf/rdf_parse.py) module.

- [Rdf Parse](#rdf-parse)
  - [_parse_events](#_parse_events)
  - [parse_dict](#parse_dict)
  - [parse_json](#parse_json)

## _parse_events

[Show source in rdf_parse.py:51](../../../prefect_meemoo/rdf/rdf_parse.py#L51)

Internal method that generates RDFlib triples
from a generator function that yields event, value pairs.

#### Signature

```python
def _parse_events(events, **kwargs): ...
```



## parse_dict

[Show source in rdf_parse.py:7](../../../prefect_meemoo/rdf/rdf_parse.py#L7)

Generates RDFlib triples from a python dictionary using a direct mapping.

#### Signature

```python
def parse_dict(data, **kwargs): ...
```



## parse_json

[Show source in rdf_parse.py:39](../../../prefect_meemoo/rdf/rdf_parse.py#L39)

Generates RDFlib triples from a file-like object
or a string using a direct mapping.

#### Signature

```python
def parse_json(json, **kwargs): ...
```