import pytest
from pytest import raises

from cabina.errors import EnvParseError
from cabina.parsers import parse_none


@pytest.mark.parametrize("value", [
    "none",
    "None",
    "null",
    "NULL",
    "Nil",
])
def test_parse_none(value):
    assert parse_none(value) is None


@pytest.mark.parametrize("value", [
    "",
    "0",
    "undefined",
])
def test_parse_invalid_none(value):
    with raises(Exception) as exc_info:
        parse_none(value)

    assert exc_info.type is EnvParseError
    assert str(exc_info.value) == f"Failed to parse {value!r} as None"
