from typing import cast

from pytest import raises

from cabina import Environment, FutureValue
from cabina.errors import EnvKeyError


def test_env_future_value_get():
    env = Environment({"<key>": "banana"})

    value = env("<key>")

    assert isinstance(value, FutureValue)
    assert value.get() == "banana"


def test_env_future_value_get_nonexisting_key():
    env = Environment({})
    value = env("<key>")
    assert isinstance(value, FutureValue)

    with raises(EnvKeyError) as exc_info:
        value.get()

    assert exc_info.type is EnvKeyError
    assert str(exc_info.value) == f"'<key>' does not exist"


def test_env_future_value_get_default_value():
    env = Environment({})

    value = env("<key>", None)
    assert isinstance(value, FutureValue)
    assert value.get() is None

    value = env("<key>", "default")
    assert isinstance(value, FutureValue)
    assert value.get() == "default"


def test_env_future_value_get_value_custom_parser():
    env = Environment({"<key>": "1234"})

    value = env("<key>", parser=int)
    assert isinstance(value, FutureValue)
    assert value.get() == 1234


def test_env_future_value_fetch():
    environ = {"<key>": "value-1"}
    env = Environment(environ)

    value = env("<key>")
    assert isinstance(value, FutureValue)
    assert value.fetch() == "value-1"

    environ["<key>"] = "value-2"
    assert value.fetch() == "value-2"


def test_env_future_value_get_cached():
    environ = {"<key>": "value-1"}
    env = Environment(environ)

    value = env("<key>")
    assert isinstance(value, FutureValue)
    assert value.get() == "value-1"

    environ["<key>"] = "value-2"
    assert value.get() == "value-1"


def test_env_raw():
    env = Environment({"<key>": "1234"})

    value = env.raw("<key>")
    assert isinstance(value, FutureValue)
    assert value.get() == "1234"


def test_env_raw_with_default():
    env = Environment({"<key1>": "1"})

    value = env.raw("<key2>", default="2")
    assert isinstance(value, FutureValue)
    assert value.get() == "2"


def test_env_none():
    env = Environment({"<key>": "None"})

    value = cast(FutureValue, env.none("<key>"))
    assert value.get() is None


def test_env_bool():
    env = Environment({"<key>": "True"})

    value = cast(FutureValue, env.bool("<key>"))
    assert value.get() is True


def test_env_int():
    env = Environment({"<key>": "42"})

    value = cast(FutureValue, env.int("<key>"))
    assert value.get() == 42


def test_env_float():
    env = Environment({"<key>": "3.14"})

    value = cast(FutureValue, env.float("<key>"))
    assert value.get() == 3.14


def test_env_str():
    env = Environment({"<key>": "banana "})

    value = cast(FutureValue, env.str("<key>"))
    assert value.get() == "banana"


def test_env_tuple():
    env = Environment({"<key>": "first, second"})

    value = cast(FutureValue, env.tuple("<key>"))
    assert value.get() == ("first", "second",)


def test_env_tuple_with_separator():
    env = Environment({"<key>": "first second"})

    value = cast(FutureValue, env.tuple("<key>", separator=" "))
    assert value.get() == ("first", "second",)


def test_env_repr():
    empty_env = Environment({})
    assert repr(empty_env) == "cabina.Environment({})"

    env = Environment({"<key>": "banana"})
    assert repr(env) == "cabina.Environment({'<key>': 'banana'})"
