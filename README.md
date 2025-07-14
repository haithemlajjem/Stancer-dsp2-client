# dsp2client

Python client library for the Stancer DSP2 API.

---

## Overview

This library provides a clean and modular Python interface to consume the Stancer DSP2 API.

It supports:

- User authentication
- Retrieving user identity details
- Accessing accounts, balances, and transactions
- Data validation and formatting using Pydantic models
- Configurable logging


---

## Requirements

- Python 3.12+
- Dependencies are managed via `pyproject.toml`


## Installation

This project uses [uv](https://github.com/jreese/uv) for dependency and environment management.

To install dependencies and set up the environment, run:

```
# Create a virtual environment
uv venv

# Activate the virtual environment (Unix/macOS)
source .venv/bin/activate


# Installs dependencies from pyproject.toml
uv pip install -e .

```


or

build the package
```
uv build
```

This generates .whl and .tar.gz files in the dist/ folder.

Then install it:

```
pip install dist/dsp2client-0.1.0*.whl
```

---
## Usage 

```python
from dsp2_client.api_client import DSP2Client

# Initialize client with user credentials
client = DSP2Client(username="mdupuis", password="111111")

# Fetch identity
identity = client.get_identity()
print(identity)

# Fetch accounts
accounts = client.get_accounts()
print(accounts)

# Fetch account
account = client.get_account(acccount_id)
print(account)

# Fetch balances
balances = client.get_balances(acccount_id)
print(balances)

# Fetch transactions
transactions = client.get_transactions(acccount_id, page, count)
print(transactions)

# Fetch full user data
full_data = client.get_full_user_data(transactions_per_account)
print(full_data)

```

---
## Running Tests

To run tests:

```
uv run pytest
```

---
## API Endpoint

The API is available at:
https://dsp2-technical-test.iliad78.net
