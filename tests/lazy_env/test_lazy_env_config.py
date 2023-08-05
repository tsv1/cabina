from pytest import raises

import cabina
from cabina import LazyEnvironment
from cabina.errors import ConfigEnvError, EnvKeyError


def test_lazy_env_config_define_nonexisting_key():
    env = LazyEnvironment({})

    class Config(cabina.Config, cabina.Section):
        API_HOST = env.str("HOST")


def test_lazy_env_config_get_nonexisting_key():
    env = LazyEnvironment({})

    class Config(cabina.Config, cabina.Section):
        API_HOST = env.str("HOST")

    with raises(Exception) as exc_info:
        Config.API_HOST

    assert exc_info.type is EnvKeyError
    assert str(exc_info.value) == "'HOST' does not exist"


def test_lazy_env_config_get_existing_key():
    env = LazyEnvironment({"HOST": "127.0.0.1"})

    class Config(cabina.Config, cabina.Section):
        API_HOST = env.str("HOST")

    assert Config.API_HOST == "127.0.0.1"


def test_lazy_env_config_get_key_nonexisting_with_default():
    env = LazyEnvironment({"API_HOST": "127.0.0.1"})

    class Config(cabina.Config, cabina.Section):
        API_HOST = env.str("HOST", default="localhost")

    assert Config.API_HOST == "localhost"


def test_lazy_env_config_prefetch():
    env = LazyEnvironment({
        "HOST": "localhost",
        "PORT": "8080",
    })

    class Config(cabina.Config, cabina.Section):
        API_HOST = env.str("HOST")
        API_PORT = env.int("PORT")

    Config.prefetch()


def test_lazy_env_config_prefetch_with_nonexisting_keys():
    env = LazyEnvironment({})

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


def test_lazy_env_config_prefetch_with_invalid_values():
    env = LazyEnvironment({"PORT": "number"})

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


def test_lazy_env_config_prefetch_with_sections():
    env = LazyEnvironment({"DEBUG": "yes"})

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
