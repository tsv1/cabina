from pytest import raises

import cabina
from cabina import Environment
from cabina.errors import EnvKeyError


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
