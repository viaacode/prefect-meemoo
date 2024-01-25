# Blocks

[Prefect-meemoo Index](../../README.md#prefect-meemoo-index) /
[Prefect Meemoo](../index.md#prefect-meemoo) /
[Config](./index.md#config) /
Blocks

> Auto-generated documentation for [prefect_meemoo.config.blocks](../../../prefect_meemoo/config/blocks.py) module.

- [Blocks](#blocks)
  - [LastRunConfig](#lastrunconfig)
    - [LastRunConfig().get_last_run](#lastrunconfig()get_last_run)

## LastRunConfig

[Show source in blocks.py:7](../../../prefect_meemoo/config/blocks.py#L7)

Block used to manage the configuration of when a flow last ran (the day).

#### Attributes

- `last_run` - The last time the flow ran.
- `flow_name` - The name of the flow.

#### Examples

Load stored LastRun configuration:

```python
from prefect_meemoo.blocks import LastRunConfig
LastRun = LastRunConfig.load("BLOCK_NAME")
last_run = LastRun.last_run
```

#### Signature

```python
class LastRunConfig(Block):
    ...
```

### LastRunConfig().get_last_run

[Show source in blocks.py:30](../../../prefect_meemoo/config/blocks.py#L30)

#### Signature

```python
def get_last_run(self, format: str = "%Y-%m-%dT%H:%M:%S.%fZ"):
    ...
```