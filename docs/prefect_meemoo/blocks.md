# Blocks

[Prefect-meemoo Index](../README.md#prefect-meemoo-index) /
[Prefect Meemoo](./index.md#prefect-meemoo) /
Blocks

> Auto-generated documentation for [prefect_meemoo.blocks](../../prefect_meemoo/blocks.py) module.

- [Blocks](#blocks)
  - [LastRunConfig](#lastrunconfig)

## LastRunConfig

[Show source in blocks.py:8](../../prefect_meemoo/blocks.py#L8)

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