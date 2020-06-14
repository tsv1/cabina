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
from cabina import computed, env


class Config(cabina.Config):
    class Main(cabina.Section):
        API_HOST: str = env.str("API_HOST", default="localhost")
        API_PORT: int = env.int("API_PORT", default=8080)

        @computed
        def API_URL(cls) -> str:
            return f"http://{cls.API_HOST}:{cls.API_PORT}"

    class Kafka(cabina.Section):
        BOOTSTRAP_SERVERS: tuple = env.tuple("KAFKA_BOOTSTRAP_SERVERS")
        AUTO_COMMIT: bool = env.bool("KAFKA_AUTO_COMMIT", True)
```

```python
assert Config.Main.API_URL == "http://localhost:8080"
assert Config["Main"]["API_URL"] == "http://localhost:8080"
```
