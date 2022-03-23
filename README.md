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
```

```python
assert Config.Main.API_URL == "http://localhost:8080"
assert Config["Main"]["API_URL"] == "http://localhost:8080"
```

### print

```python
print(Config)
# class <Config>:
#     class <Main>:
#         API_HOST = 'localhost'
#         API_PORT = 8080
#         API_URL = 'http://localhost:8080'
```

## Recipes

* [Root Section](#root-section)
* [Computed Values](#computed-values)
* [Default Values](#default-values)
* [Raw Values](#raw-values)
* [Custom Parsers](#custom-parsers)
* [JSON Parser](#json-parser)
* [Prefetch Env Vars](#prefetch-env-vars)
* [Env Vars Prefix](#env-vars-prefix)
* [Inheritance](#inheritance)


### Root Section

```sh
export API_HOST=localhost;
export API_PORT=8080;
```

```python
import cabina
from cabina import env


class Config(cabina.Config, cabina.Section):  # <- inherited from cabina.Section
    API_HOST = env.str("API_HOST")
    API_PORT = env.int("API_PORT")


assert Config.API_HOST == "localhost"
assert Config.API_PORT == 8080
```


### Computed Values

```sh
export API_HOST=localhost;
export API_PORT=8080;
```

```python
import cabina
from cabina import computed, env


class Config(cabina.Config, cabina.Section):
    API_HOST: str = env.str("API_HOST")
    API_PORT: int = env.int("API_PORT")

    @computed
    def API_URL(cls) -> str:
        return f"http://{cls.API_HOST}:{cls.API_PORT}"


assert Config.API_URL == "http://localhost:8080"
```


### Default Values

```sh
export API_HOST=127.0.0.1;
```

```python
import cabina
from cabina import env


class Config(cabina.Config, cabina.Section):
    API_HOST = env.str("API_HOST", default="localhost")  # <- default arg
    API_PORT = env.int("API_PORT", default=8080)


assert Config.API_HOST == "127.0.0.1"
assert Config.API_PORT == 8080
```


### Raw Values

```sh
export DEBUG= yes;
#            ^ extra space
```

```python
import cabina
from cabina import env


class Config(cabina.Config, cabina.Section):
    DEBUG_RAW = env.raw("DEBUG")  # <- alias to env("DEBUG")
    DEBUG_STR = env.str("DEBUG")


assert Config.DEBUG_RAW == ""  # True
assert Config.DEBUG_STR == "yes"  # Error
```


### Custom Parsers

```sh
export HTTP_TIMEOUT=10s;
```

```python
import cabina
from cabina import env
from pytimeparse import parse as parse_duration  # <- external package


class Config(cabina.Config, cabina.Section):
    HTTP_TIMEOUT: int = env("HTTP_TIMEOUT", parser=parse_duration)


assert Config.HTTP_TIMEOUT == 10
```


### JSON Parser

```sh
export IMAGE_SETTINGS='{"AllowedContentTypes": ["image/png", "image/jpeg"]}';
```

```python
import json

import cabina
from cabina import env


class Config(cabina.Config, cabina.Section):
    IMAGE_SETTINGS = env("IMAGE_SETTINGS", parser=json.loads)  # <- json.loads


assert Config.IMAGE_SETTINGS == {
    'AllowedContentTypes': ['image/png', 'image/jpeg']
}
```


### Prefetch Env Vars

```sh
export DEBUG=yes;
export API_PORT=80a;  # <- extra "a"
```

```python
import cabina
from cabina import env


class Config(cabina.Config, cabina.Section):
    DEBUG = env.bool("DEBUG")
    API_HOST = env.str("API_HOST")
    API_PORT = env.int("API_PORT")


Config.prefetch()  # <- prefetch method

# ConfigEnvError: Failed to prefetch:
# - Config.API_HOST: 'API_HOST' does not exist
# - Config.API_PORT: Failed to parse '80a' as int
```


### Env Vars Prefix

```sh
export APP_HOST=localhost;
export APP_PORT=8080;
```

```python
import cabina

env = cabina.Environment(prefix="APP_")


class Config(cabina.Config, cabina.Section):
    API_HOST = env.str("HOST")  # <- No "APP_" prefix
    API_PORT = env.int("PORT")


assert Config.API_HOST == "localhost"
assert Config.API_PORT == 8080
```


### Inheritance

```python
import cabina


class Config(cabina.Config, cabina.Section):
    DEBUG = False

    class Api(cabina.Section):
        API_HOST = "app.dev"
        API_PORT = 5000


class ConfigLocal(Config):
    DEBUG = True

    class Api(Config.Api):
        API_HOST = "localhost"


assert ConfigLocal.DEBUG is True
assert ConfigLocal.Api.API_HOST == "localhost"
assert ConfigLocal.Api.API_PORT == 5000
```
