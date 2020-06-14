import pytest
from pytest import raises

from cabina.errors import EnvParseError
from cabina.parsers import parse_bool


@pytest.mark.parametrize("value", [
    "y",
    "yes",
    "t",
    "true",
    "on",
    "1",
])
def test_parse_truthy_bool(value):
    assert parse_bool(value) is True


@pytest.mark.parametrize("value", [
    "n",
    "no",
    "f",
    "false",
    "off",
    "0",
])
def test_parse_falsy_bool(value):
    assert parse_bool(value) is False


@pytest.mark.parametrize("value", [
    "",
    "42",
    "banana",
])
def test_parse_invalid_bool(value):
    with raises(Exception) as exc_info:
        parse_bool(value)

    assert exc_info.type is EnvParseError
    assert str(exc_info.value) == f"Failed to parse {value!r} as bool"
