# Tasks

[Prefect-meemoo Index](../../README.md#prefect-meemoo-index) / [Prefect Meemoo](../index.md#prefect-meemoo) / [Rabbitmq](./index.md#rabbitmq) / Tasks

> Auto-generated documentation for [prefect_meemoo.rabbitmq.tasks](../../../prefect_meemoo/rabbitmq/tasks.py) module.

- [Tasks](#tasks)
  - [declare_queue](#declare_queue)
  - [init_channel](#init_channel)
  - [init_connection](#init_connection)
  - [init_credentials](#init_credentials)
  - [publish](#publish)

## declare_queue

[Show source in tasks.py:29](../../../prefect_meemoo/rabbitmq/tasks.py#L29)

#### Signature

```python
@task(name="Declare queue")
def declare_queue(channel, queue, exchange): ...
```



## init_channel

[Show source in tasks.py:21](../../../prefect_meemoo/rabbitmq/tasks.py#L21)

#### Signature

```python
@task(name="Init channel")
def init_channel(connection): ...
```



## init_connection

[Show source in tasks.py:12](../../../prefect_meemoo/rabbitmq/tasks.py#L12)

#### Signature

```python
@task(name="Init connection")
def init_connection(host, port, credentials): ...
```



## init_credentials

[Show source in tasks.py:6](../../../prefect_meemoo/rabbitmq/tasks.py#L6)

#### Signature

```python
def init_credentials(user, password): ...
```



## publish

[Show source in tasks.py:38](../../../prefect_meemoo/rabbitmq/tasks.py#L38)

#### Signature

```python
@task(name="Publish message")
def publish(channel, exchange, queue, message): ...
```