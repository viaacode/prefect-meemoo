# Blocks

[Prefect-meemoo Index](../../README.md#prefect-meemoo-index) / [Prefect Meemoo](../index.md#prefect-meemoo) / [Config](./index.md#config) / Blocks

> Auto-generated documentation for [prefect_meemoo.config.blocks](../../../prefect_meemoo/config/blocks.py) module.

- [Blocks](#blocks)
  - [LastRunConfig](#lastrunconfig)
    - [LastRunConfig().add_last_run](#lastrunconfig()add_last_run)
    - [LastRunConfig().get_last_run](#lastrunconfig()get_last_run)

## LastRunConfig

[Show source in blocks.py:11](../../../prefect_meemoo/config/blocks.py#L11)

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
class LastRunConfig(Block): ...
```

### LastRunConfig().add_last_run

[Show source in blocks.py:47](../../../prefect_meemoo/config/blocks.py#L47)

#### Signature

```python
def add_last_run(self, context: str = "", time: pendulum.DateTime = None): ...
```

### LastRunConfig().get_last_run

[Show source in blocks.py:39](../../../prefect_meemoo/config/blocks.py#L39)

#### Signature

```python
def get_last_run(self, format: str = "%Y-%m-%dT%H:%M:%S.%fZ", context: str = ""): ...
```