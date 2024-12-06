# Qiscus SDK

Qiscus SDK is a Python library for interacting with Qiscus API, supporting both synchronous and asynchronous clients.

## Installation

To install the library, run the following command:

```bash
pip install qiscus-python-sdk
```


## Usage

```python
from qiscus_python_sdk.auth import get_auth

# Synchronous Authentication
auth = get_auth(client_type="sync")
response = auth.login("user@example.com", "password")
print(response)

# Asynchronous Authentication
import asyncio
async def main():
    auth = get_auth(client_type="async")
    response = await auth.login("user@example.com", "password")
    print(response)

asyncio.run(main())
