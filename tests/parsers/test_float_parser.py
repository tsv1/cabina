import sys
from math import isnan

import pytest
from pytest import raises

from cabina.errors import EnvParseError
from cabina.parsers import parse_float


@pytest.mark.parametrize(("value", "expected"), [
    ("+3.14", 3.14),
    ("3.14", 3.14),
    ("-3.14", -3.14),
    (".14", 0.14),
    ("3.", 3.0),
    ("0.0", 0.0),
    ("1", 1),
    ("-1", -1),
    ("0", 0),
    ("Infinity", float("inf")),
    ("INFINITY", float("inf")),
    ("inf", float("inf")),
    ("+inf", float("inf")),
    ("-inf", float("-inf")),
    (str(sys.float_info.min), sys.float_info.min),
    (str(sys.float_info.max), sys.float_info.max),
])
def test_parse_float(value, expected):
    assert parse_float(value) == expected


@pytest.mark.parametrize("value", [
    "nan",
    "Nan",
])
def test_parse_float_nan(value):
    assert isnan(parse_float(value))


@pytest.mark.parametrize("value", [
    "",
    ".",
    "3.14.5",
    "3.14a",
    "--3.14",
])
def test_parse_invalid_float(value):
    with raises(Exception) as exc_info:
        parse_float(value)

    assert exc_info.type is EnvParseError
    assert str(exc_info.value) == f"Failed to parse {value!r} as float"
