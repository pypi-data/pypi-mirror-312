# Stub File for python-decouple

This package enables static type checking for parameters retrieved from the config in the [python-decouple](https://pypi.org/project/python-decouple/) library.

Tested with [basedpyright 1.15.2](https://pypi.org/project/basedpyright/)

[Github](https://github.com/tobievil/decouple-stubs)

## Installation

I recommend adding this package only in the development environment and not in production as it does nothing at runtime.

```bash
# using pip
pip3 install python-decople-stubs

# using poetry
poetry install python-decople
poetry install python-decople-stubs --group=dev
```

## Examples

```python
import datetime
import enum
import os

import decouple

config = decouple.config


def test_str():
    os.environ["var"] = "test_string"
    var = config("var")
    return var  # var is str


def test_int():
    os.environ["var"] = "42069"
    var = config("var", cast=int)
    return var  # var is int


def test_date():
    os.environ["var"] = "3000-01-01"
    var = config("var", cast=datetime.date.fromisoformat)
    return var  # var is date


def test_default_none():
    os.environ["var"] = "test_string"
    var = config("var", default=None)
    return var  # var is union of str and None


def test_default_int_float():
    os.environ["var"] = "42"
    var = config("var", default=42.69, cast=int)
    return var  # var is union of float and int


class ConnectionOptions(enum.Enum):
    usb = "usb"
    eth = "eth"
    bluetooth = "bluetooth"


def test_enum():
    os.environ["CONNECTION_TYPE"] = "bluetooth"
    var = config("CONNECTION_TYPE", cast=ConnectionOptions)
    assert ConnectionOptions.bluetooth == var
    return var  # var is member of Enum ConnectionOptions
```
