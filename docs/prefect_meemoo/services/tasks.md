# Tasks

[Prefect-meemoo Index](../../README.md#prefect-meemoo-index) /
[Prefect Meemoo](../index.md#prefect-meemoo) /
[Services](./index.md#services) /
Tasks

> Auto-generated documentation for [prefect_meemoo.services.tasks](../../../prefect_meemoo/services/tasks.py) module.

- [Tasks](#tasks)
  - [sync_etl_service](#sync_etl_service)

## sync_etl_service

[Show source in tasks.py:16](../../../prefect_meemoo/services/tasks.py#L16)

Task that runs an ETL service over HTTP.

#### Arguments

- `api_server` *str* - URL of the service
- `api_route` *str* - API route to run
- `last_modified` *str* - A datetime indicating when the ETL was last run

#### Returns

- `_type_` - _description_

#### Signature

```python
@task(
    name="Run HTTP ETL service",
    description="Runs an ETL service that is exposed by HTTP API.",
)
def sync_etl_service(api_server: str, api_route: str, last_modified: str):
    ...
```