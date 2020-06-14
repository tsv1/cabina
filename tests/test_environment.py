from pytest import raises

from cabina import Environment
from cabina._environment import EnvKeyError


def test_env():
    env = Environment({"<key>": "banana"})
    assert env("<key>") == "banana"


def test_env_nonexisting_key():
    env = Environment({})

    with raises(EnvKeyError) as exc_info:
        env("<key>")

    assert exc_info.type is EnvKeyError
    assert str(exc_info.value) == f"'<key>'"


def test_env_default_value():
    env = Environment({})

    assert env("<key>", None) is None
    assert env("<key>", "default") == "default"


def test_env_none():
    env = Environment({"<key>": "None"})
    assert env.none("<key>") is None


def test_env_bool():
    env = Environment({"<key>": "True"})
    assert env.bool("<key>") is True


def test_env_int():
    env = Environment({"<key>": "42"})
    assert env.int("<key>") == 42


def test_env_float():
    env = Environment({"<key>": "3.14"})
    assert env.float("<key>") == 3.14


def test_env_str():
    env = Environment({"<key>": "banana "})
    assert env.str("<key>") == "banana"


def test_env_tuple():
    env = Environment({"<key>": "first, second"})
    assert env.tuple("<key>") == ("first", "second",)


def test_env_tuple_with_separator():
    env = Environment({"<key>": "first second"})
    assert env.tuple("<key>", separator=" ") == ("first", "second",)
