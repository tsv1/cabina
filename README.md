# cabina

[![Codecov](https://img.shields.io/codecov/c/github/nikitanovosibirsk/cabina/master.svg?style=flat-square)](https://codecov.io/gh/nikitanovosibirsk/cabina)
[![PyPI](https://img.shields.io/pypi/v/cabina.svg?style=flat-square)](https://pypi.python.org/pypi/cabina/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/cabina?style=flat-square)](https://pypi.python.org/pypi/cabina/)
[![Python Version](https://img.shields.io/pypi/pyversions/cabina.svg?style=flat-square)](https://pypi.python.org/pypi/cabina/)

## Installation

```sh
pip3 install cabina
```

## Usage

```python
import cabina


class Config(cabina.Config):
    class Main(cabina.Section):
        API_HOST: str = "localhost"
        API_PORT: int = 8080

    class Db(cabina.Section):
        host: str = "localhost"
        port: int = 5432
        username: str = "postgres"
        password: str = ""
```

```python
assert Config.Main.API_HOST == "localhost"
assert Config["Main"]["API_HOST"] == "localhost"
```
