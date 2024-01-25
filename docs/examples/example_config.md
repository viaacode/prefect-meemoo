# Example Config

[Prefect-meemoo Index](../README.md#prefect-meemoo-index) /
[Examples](./index.md#examples) /
Example Config

> Auto-generated documentation for [examples.example_config](../../examples/example_config.py) module.

- [Example Config](#example-config)
  - [last_modified_config](#last_modified_config)

## last_modified_config

[Show source in example_config.py:8](../../examples/example_config.py#L8)

#### Examples

Configure a flow to save the last run config:

```python
@flow(name="prefect_flow_test", on_completion=[save_last_run_config])
def last_modified_config(
    full_sync: bool = False,
):
    logger = get_run_logger()
    logger.info(get_last_run_config())
    date = get_last_run_config()
```

#### Signature

```python
@flow(name="last_modified_config", on_completion=[save_last_run_config])
def last_modified_config(full_sync: bool = False):
    ...
```