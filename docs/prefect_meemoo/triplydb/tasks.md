# Tasks

[Prefect-meemoo Index](../../README.md#prefect-meemoo-index) /
[Prefect Meemoo](../index.md#prefect-meemoo) /
[Triplydb](./index.md#triplydb) /
Tasks

> Auto-generated documentation for [prefect_meemoo.triplydb.tasks](../../../prefect_meemoo/triplydb/tasks.py) module.

- [Tasks](#tasks)
  - [run_triplyetl](#run_triplyetl)

## run_triplyetl

[Show source in tasks.py:13](../../../prefect_meemoo/triplydb/tasks.py#L13)

#### Signature

```python
@task(
    name="Run TriplyETL",
    description="Runs an TriplyETL script.",
    task_run_name="{task_run_name}",
)
def run_triplyetl(etl_script_path: str, task_run_name: str = "Run TriplyETL", **kwargs):
    ...
```