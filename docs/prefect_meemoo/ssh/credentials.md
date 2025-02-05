# Credentials

[Prefect-meemoo Index](../../README.md#prefect-meemoo-index) / [Prefect Meemoo](../index.md#prefect-meemoo) / [Ssh](./index.md#ssh) / Credentials

> Auto-generated documentation for [prefect_meemoo.ssh.credentials](../../../prefect_meemoo/ssh/credentials.py) module.

- [Credentials](#credentials)
  - [SSHCredentials](#sshcredentials)
    - [SSHCredentials().get_client](#sshcredentials()get_client)

## SSHCredentials

[Show source in credentials.py:11](../../../prefect_meemoo/ssh/credentials.py#L11)

Block used to manage authentication with SSH.

#### Attributes

- `password` - SSH password
- `user` - remote SSH user
- `host` - remote SSH host
- `post` - SSH port

#### Examples

Load stored SSH credentials:

```python
from prefect_meemoo.ssh import SSHCredentials
credentials = SSHCredentials.load("BLOCK_NAME")
```

#### Signature

```python
class SSHCredentials(Block): ...
```

### SSHCredentials().get_client

[Show source in credentials.py:50](../../../prefect_meemoo/ssh/credentials.py#L50)

Helper method to get a SSH client and establish a connection.

#### Returns

- A connected SSH client

#### Signature

```python
def get_client(self) -> SSHClient: ...
```