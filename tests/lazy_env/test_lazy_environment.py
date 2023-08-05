from typing import cast

from pytest import raises

from cabina import FutureValue, LazyEnvironment
from cabina.errors import EnvKeyError


def test_lazy_env_future_value_get():
    env = LazyEnvironment({"<key>": "banana"})

    value = env("<key>")

    assert isinstance(value, FutureValue)
    assert value.get() == "banana"


def test_lazy_env_future_value_get_nonexisting_key():
    env = LazyEnvironment({})
    value = env("<key>")
    assert isinstance(value, FutureValue)

    with raises(EnvKeyError) as exc_info:
        value.get()

    assert exc_info.type is EnvKeyError
    assert str(exc_info.value) == "'<key>' does not exist"


def test_lazy_env_future_value_get_default_value():
    env = LazyEnvironment({})

    value = env("<key>", None)
    assert isinstance(value, FutureValue)
    assert value.get() is None

    value = env("<key>", "default")
    assert isinstance(value, FutureValue)
    assert value.get() == "default"


def test_lazy_env_future_value_get_value_custom_parser():
    env = LazyEnvironment({"<key>": "1234"})

    value = env("<key>", parser=int)
    assert isinstance(value, FutureValue)
    assert value.get() == 1234


def test_lazy_env_future_value_fetch():
    environ = {"<key>": "value-1"}
    env = LazyEnvironment(environ)

    value = env("<key>")
    assert isinstance(value, FutureValue)
    assert value.fetch() == "value-1"

    environ["<key>"] = "value-2"
    assert value.fetch() == "value-2"


def test_lazy_env_future_value_get_cached():
    environ = {"<key>": "value-1"}
    env = LazyEnvironment(environ)

    value = env("<key>")
    assert isinstance(value, FutureValue)
    assert value.get() == "value-1"

    environ["<key>"] = "value-2"
    assert value.get() == "value-1"


def test_lazy_env_get():
    env = LazyEnvironment({"<key>": "1234"})
    assert env.get("<key>") == "1234"


def test_lazy_env_get_with_parser():
    env = LazyEnvironment({"<key>": "1234"})
    assert env.get("<key>", parser=int) == 1234


def test_lazy_env_get_with_default():
    env = LazyEnvironment({})
    assert env.get("<key>", default=None) is None
    assert env.get("<key>", default="banana") == "banana"


def test_lazy_env_raw():
    env = LazyEnvironment({"<key>": "1234"})

    value = env.raw("<key>")
    assert isinstance(value, FutureValue)
    assert value.get() == "1234"


def test_lazy_env_raw_with_default():
    env = LazyEnvironment({"<key1>": "1"})

    value = env.raw("<key2>", default="2")
    assert isinstance(value, FutureValue)
    assert value.get() == "2"


def test_lazy_env_none():
    env = LazyEnvironment({"<key>": "None"})

    value = cast(FutureValue, env.none("<key>"))
    assert value.get() is None


def test_lazy_env_none_incorrect_default():
    env = LazyEnvironment({})
    with raises(AssertionError):
        env.none("<key>", default="None")


def test_lazy_env_bool():
    env = LazyEnvironment({"<key>": "True"})

    value = cast(FutureValue, env.bool("<key>"))
    assert value.get() is True


def test_lazy_env_bool_incorrect_default():
    env = LazyEnvironment({})
    with raises(AssertionError):
        env.bool("<key>", default="True")


def test_lazy_env_int():
    env = LazyEnvironment({"<key>": "42"})

    value = cast(FutureValue, env.int("<key>"))
    assert value.get() == 42


def test_lazy_env_int_incorrect_default():
    env = LazyEnvironment({})
    with raises(AssertionError):
        env.int("<key>", default="42")


def test_lazy_env_float():
    env = LazyEnvironment({"<key>": "3.14"})

    value = cast(FutureValue, env.float("<key>"))
    assert value.get() == 3.14


def test_lazy_env_float_incorrect_default():
    env = LazyEnvironment({})
    with raises(AssertionError):
        env.float("<key>", default="3.14")


def test_lazy_env_str():
    env = LazyEnvironment({"<key>": "banana "})

    value = cast(FutureValue, env.str("<key>"))
    assert value.get() == "banana"


def test_lazy_env_str_incorrect_default():
    env = LazyEnvironment({})
    with raises(AssertionError):
        env.str("<key>", default=None)


def test_lazy_env_tuple():
    env = LazyEnvironment({"<key>": "first, second"})

    value = cast(FutureValue, env.tuple("<key>"))
    assert value.get() == ("first", "second",)


def test_lazy_env_tuple_incorrect_default():
    env = LazyEnvironment({})
    with raises(AssertionError):
        env.tuple("<key>", default=[])


def test_lazy_env_tuple_with_separator():
    env = LazyEnvironment({"<key>": "first second"})

    value = cast(FutureValue, env.tuple("<key>", separator=" "))
    assert value.get() == ("first", "second",)


def test_lazy_env_repr():
    empty_env = LazyEnvironment({})
    assert repr(empty_env) == "cabina.LazyEnvironment({})"

    env = LazyEnvironment({"<key>": "banana"})
    assert repr(env) == "cabina.LazyEnvironment({'<key>': 'banana'})"


def test_lazy_env_prefix():
    env = LazyEnvironment({"APP_NAME": "banana"}, prefix="APP_")
    assert env("NAME").get() == "banana"
    assert env.get("NAME") == "banana"
