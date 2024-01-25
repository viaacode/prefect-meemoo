# Last Run

[Prefect-meemoo Index](../../README.md#prefect-meemoo-index) /
[Prefect Meemoo](../index.md#prefect-meemoo) /
[Config](./index.md#config) /
Last Run

> Auto-generated documentation for [prefect_meemoo.config.last_run](../../../prefect_meemoo/config/last_run.py) module.

- [Last Run](#last-run)
  - [get_last_run_config](#get_last_run_config)
  - [save_last_run_config](#save_last_run_config)

## get_last_run_config

[Show source in last_run.py:36](../../../prefect_meemoo/config/last_run.py#L36)

Get the last run config for a flow.
If the flow is run with the parameter `full_sync` and it is True, the last run config is ignored.

#### Arguments

- `format` *str* - format of the returned timestamp

#### Returns

The datetime of the last run config or None if no last run config is found.

#### Examples

Configure a flow to get the last run config:

```python
@flow(name="prefect_flow_test", on_completion=[save_last_run_config])
def main_flow(
    full_sync: bool = True,
):
    logger = get_run_logger()
    logger.info("test")
    logger.info(get_last_run_config())
```

#### Signature

```python
def get_last_run_config(format="%Y-%m-%dT%H:%M:%S.%fZ"):
    ...
```



## save_last_run_config

[Show source in last_run.py:7](../../../prefect_meemoo/config/last_run.py#L7)

Save the last run config for a flow.

Result:
    The last run config is saved in a block in the prefect server.
    The name of the block is the name of the deployment + "-lastmodified".

#### Examples

Configure a flow to save the last run config:

```python
@flow(name="prefect_flow_test", on_completion=[save_last_run_config])
def main_flow(
    full_sync: bool = False,
):
    logger = get_run_logger()
    logger.info("test")
    logger.info(get_last_run_config())
```

#### Signature

```python
def save_last_run_config(flow: Flow, flow_run: FlowRun, state):
    ...
```