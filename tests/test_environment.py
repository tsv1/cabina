import sys

import pytest

from cabina import Environment


def test_env():
    value = "val"
    env = Environment({"key": value})
    assert env("key") == value


@pytest.mark.parametrize("value", [
    "none",
    "None",
    "null",
    "NULL",
    "Nil",
])
def test_env_none(value):
    env = Environment({"key": value})
    assert env.none("key") is None


@pytest.mark.parametrize("value", [
    "y",
    "yes",
    "t",
    "true",
    "on",
    "1",
])
def test_env_bool_true(value):
    env = Environment({"key": value})
    assert env.bool("key") is True


@pytest.mark.parametrize("value", [
    "n",
    "no",
    "f",
    "false",
    "off",
    "0",
])
def test_env_bool_false(value):
    env = Environment({"key": value})
    assert env.bool("key") is False


@pytest.mark.parametrize(("value", "expected"), [
    ("1", 1),
    ("-1", -1),
    ("0", 0),
    (str(sys.maxsize), sys.maxsize),
    (str(-sys.maxsize - 1), -sys.maxsize - 1),
])
def test_env_int(value, expected):
    env = Environment({"key": value})
    assert env.int("key") == expected


@pytest.mark.parametrize(("value", "expected"), [
    ("3.14", 3.14),
    ("-3.14", -3.14),
    ("0.0", 0.0),
    ("1", 1),
    ("-1", -1),
    ("0", 0),
    ("inf", float("inf")),
    ("+inf", float("inf")),
    ("-inf", float("-inf")),
])
def test_env_float(value, expected):
    env = Environment({"key": value})
    assert env.float("key") == expected


def test_env_str():
    value = "val"
    env = Environment({"key": value})
    assert env.str("key") == value
