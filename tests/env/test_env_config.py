from pytest import raises

import cabina
from cabina import Environment, LazyEnvironment
from cabina.errors import ConfigEnvError, EnvKeyError


def test_env_config_define_nonexisting_key():
    env = Environment({})

    with raises(Exception) as exc_info:
        class Config(cabina.Config, cabina.Section):
            API_HOST = env.str("HOST")

    assert exc_info.type is EnvKeyError
    assert str(exc_info.value) == "$HOST does not exist"


def test_env_config_get_existing_key():
    env = Environment({"HOST": "127.0.0.1"})

    class Config(cabina.Config, cabina.Section):
        API_HOST = env.str("HOST")

    assert Config.API_HOST == "127.0.0.1"


def test_env_config_get_key_nonexisting_with_default():
    env = Environment({"API_HOST": "127.0.0.1"})

    class Config(cabina.Config, cabina.Section):
        API_HOST = env.str("HOST", default="localhost")

    assert Config.API_HOST == "localhost"


def test_env_config_prefetch():
    env = Environment({
        "HOST": "localhost",
        "PORT": "8080",
    })

    class Config(cabina.Config, cabina.Section):
        API_HOST = env.str("HOST")
        API_PORT = env.int("PORT")

    Config.prefetch()


def test_env_config_prefetch_with_nonexisting_keys():
    environ = {"DEBUG": "true"}
    env = Environment(environ)
    lazy_env = LazyEnvironment(environ)

    class Config(cabina.Config, cabina.Section):
        API_HOST = lazy_env.str("HOST")
        API_PORT = lazy_env.int("PORT")
        DEBUG = env.bool("DEBUG")

    with raises(Exception) as exc_info:
        Config.prefetch()

    message = "\n".join([
        "Failed to prefetch:",
        "- Config.API_HOST: $HOST does not exist",
        "- Config.API_PORT: $PORT does not exist",
    ])
    assert exc_info.type is ConfigEnvError
    assert str(exc_info.value) == message


def test_env_config_prefetch_with_invalid_values():
    environ = {"DEBUG": "true", "PORT": "number"}
    env = Environment(environ)
    lazy_env = LazyEnvironment(environ)

    class Config(cabina.Config, cabina.Section):
        API_HOST = lazy_env.str("HOST")
        API_PORT = lazy_env.int("PORT")
        DEBUG = env.bool("DEBUG")

    with raises(Exception) as exc_info:
        Config.prefetch()

    message = "\n".join([
        "Failed to prefetch:",
        "- Config.API_HOST: $HOST does not exist",
        "- Config.API_PORT: Failed to parse 'number' as int",
    ])
    assert exc_info.type is ConfigEnvError
    assert str(exc_info.value) == message
