from pytest import raises

import cabina
from cabina import LazyEnvironment
from cabina.errors import EnvKeyError


def test_lazy_env_section_define_nonexisting_key():
    env = LazyEnvironment({})

    class Section(cabina.Section):
        API_HOST = env.str("HOST")


def test_lazy_env_section_get_nonexisting_key():
    env = LazyEnvironment({})

    class Section(cabina.Section):
        API_HOST = env.str("HOST")

    with raises(Exception) as exc_info:
        Section.API_HOST

    assert exc_info.type is EnvKeyError
    assert str(exc_info.value) == "'HOST' does not exist"


def test_lazy_env_section_get_existing_key():
    env = LazyEnvironment({"HOST": "127.0.0.1"})

    class Section(cabina.Section):
        API_HOST = env.str("HOST")

    assert Section.API_HOST == "127.0.0.1"


def test_lazy_env_section_get_key_nonexisting_with_default():
    env = LazyEnvironment({"API_HOST": "127.0.0.1"})

    class Section(cabina.Section):
        API_HOST = env.str("HOST", default="localhost")

    assert Section.API_HOST == "localhost"
