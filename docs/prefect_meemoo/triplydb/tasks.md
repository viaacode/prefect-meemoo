# Tasks

[Prefect-meemoo Index](../../README.md#prefect-meemoo-index) / [Prefect Meemoo](../index.md#prefect-meemoo) / [Triplydb](./index.md#triplydb) / Tasks

> Auto-generated documentation for [prefect_meemoo.triplydb.tasks](../../../prefect_meemoo/triplydb/tasks.py) module.

- [Tasks](#tasks)
  - [run_javascript](#run_javascript)
  - [run_terminal](#run_terminal)
  - [run_triplyetl](#run_triplyetl)

## run_javascript

[Show source in tasks.py:59](../../../prefect_meemoo/triplydb/tasks.py#L59)

#### Signature

```python
@task(
    name="Run JavaScript",
    description="Runs an JavaScript script with NodeJS.",
    task_run_name="{task_run_name}",
)
def run_javascript(
    script_path: str,
    task_run_name: str = "Run JavaScript",
    base_path=os.getcwd(),
    n_lines_after_fail=30,
    **kwargs
): ...
```



## run_terminal

[Show source in tasks.py:86](../../../prefect_meemoo/triplydb/tasks.py#L86)

#### Signature

```python
def run_terminal(
    command,
    cwd: str = os.getcwd(),
    base_path=os.getcwd(),
    on_error=None,
    n_lines_after_fail=30,
    **kwargs
): ...
```



## run_triplyetl

[Show source in tasks.py:19](../../../prefect_meemoo/triplydb/tasks.py#L19)

#### Signature

```python
@task(
    name="Run TriplyETL",
    description="Runs an TriplyETL script.",
    task_run_name="{task_run_name}",
)
def run_triplyetl(
    etl_script_path: str,
    task_run_name: str = "Run TriplyETL",
    base_path=os.getcwd(),
    n_lines_after_fail=30,
    **kwargs
): ...
```