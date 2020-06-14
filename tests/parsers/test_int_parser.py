import sys

import pytest
from pytest import raises

from cabina.errors import EnvParseError
from cabina.parsers import parse_int


@pytest.mark.parametrize(("value", "expected"), [
    ("1", 1),
    ("+1", 1),
    ("-1", -1),
    ("0", 0),
    (str(sys.maxsize), sys.maxsize),
    (str(-sys.maxsize - 1), -sys.maxsize - 1),
])
def test_parse_int(value, expected):
    assert parse_int(value) == expected


@pytest.mark.parametrize(("value", "base", "expected"), [
    ("00111", 2, 7),
    ("011", 36, 37),
    ("42", 0, 42),
])
def test_parse_int_with_base(value, base, expected):
    assert parse_int(value, base=base) == expected


@pytest.mark.parametrize("value", [
    "",
    "+",
    "12a",
    "--1234",
    "3.14",
])
def test_parse_invalid_int(value):
    with raises(Exception) as exc_info:
        parse_int(value)

    assert exc_info.type is EnvParseError
    assert str(exc_info.value) == f"Failed to parse {value!r} as int"


@pytest.mark.parametrize(("value", "base"), [
    ("011", -1),
    ("011", 0),
    ("011", 1),
    ("011", 37),
])
def test_parse_int_with_invalid_base(value, base):
    with raises(Exception) as exc_info:
        parse_int(value, base=base)

    assert exc_info.type is EnvParseError
    assert str(exc_info.value) == f"Failed to parse {value!r} as int with base {base}"
