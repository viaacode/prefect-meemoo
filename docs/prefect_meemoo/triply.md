# Triply

[Prefect-meemoo Index](../README.md#prefect-meemoo-index) /
[Prefect Meemoo](./index.md#prefect-meemoo) /
Triply

> Auto-generated documentation for [prefect_meemoo.triply](../../prefect_meemoo/triply.py) module.

- [Triply](#triply)
  - [run_triplyetl](#run_triplyetl)

## run_triplyetl

[Show source in triply.py:11](../../prefect_meemoo/triply.py#L11)

#### Signature

```python
@task(name="Run TriplyETL", description="Runs an TriplyETL script.")
def run_triplyetl(etl_script_path: str, **kwargs):
    ...
```