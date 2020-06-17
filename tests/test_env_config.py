from pytest import raises

import cabina
from cabina import Environment
from cabina.errors import ConfigEnvError, EnvKeyError


def test_env_config_define_nonexisting_key():
    env = Environment({})

    class Config(cabina.Config, cabina.Section):
        API_HOST = env.str("HOST")


def test_env_config_get_nonexisting_key():
    env = Environment({})

    class Config(cabina.Config, cabina.Section):
        API_HOST = env.str("HOST")

    with raises(Exception) as exc_info:
        Config.API_HOST

    assert exc_info.type is EnvKeyError
    assert str(exc_info.value) == f"'HOST' does not exist"


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
    env = Environment({})

    class Config(cabina.Config, cabina.Section):
        API_HOST = env.str("HOST")
        API_PORT = env.int("PORT")

    with raises(Exception) as exc_info:
        Config.prefetch()

    message = "\n".join([
        "Failed to prefetch:",
        "- Config.API_HOST: 'HOST' does not exist",
        "- Config.API_PORT: 'PORT' does not exist",
    ])
    assert exc_info.type is ConfigEnvError
    assert str(exc_info.value) == message


def test_env_config_prefetch_with_invalid_values():
    env = Environment({"PORT": "number"})

    class Config(cabina.Config, cabina.Section):
        API_HOST = env.str("HOST")
        API_PORT = env.int("PORT")

    with raises(Exception) as exc_info:
        Config.prefetch()

    message = "\n".join([
        "Failed to prefetch:",
        "- Config.API_HOST: 'HOST' does not exist",
        "- Config.API_PORT: Failed to parse 'number' as int",
    ])
    assert exc_info.type is ConfigEnvError
    assert str(exc_info.value) == message


def test_env_config_prefetch_with_sections():
    env = Environment({"DEBUG": "yes"})

    class Config(cabina.Config, cabina.Section):
        TZ = env.str("TZ")
        DEBUG = env.bool("DEBUG")

        class Main(cabina.Section):
            API_HOST = env.str("HOST", default="localhost")
            API_PORT = env.int("PORT")

    with raises(Exception) as exc_info:
        Config.prefetch()

    message = "\n".join([
        "Failed to prefetch:",
        "- Config.TZ: 'TZ' does not exist",
        "- Config.Main.API_PORT: 'PORT' does not exist",
    ])
    assert exc_info.type is ConfigEnvError
    assert str(exc_info.value) == message
