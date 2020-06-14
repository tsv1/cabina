import sys
from math import isnan

import pytest

from cabina._parsers import (
    parse_as_is,
    parse_bool,
    parse_float,
    parse_int,
    parse_none,
    parse_str,
    parse_tuple,
)


@pytest.mark.parametrize("value", [
    "None",
    "True",
    "42",
    "3.14",
    "banana",
])
def test_parse_as_is(value):
    assert parse_as_is(value) == value


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


def test_parse_int_with_base():
    assert parse_int("00111", base=2) == 7


@pytest.mark.parametrize(("value", "expected"), [
    ("+3.14", 3.14),
    ("3.14", 3.14),
    ("-3.14", -3.14),
    ("0.0", 0.0),
    ("1", 1),
    ("-1", -1),
    ("0", 0),
    ("Infinity", float("inf")),
    ("INFINITY", float("inf")),
    ("inf", float("inf")),
    ("+inf", float("inf")),
    ("-inf", float("-inf")),
])
def test_parse_float(value, expected):
    assert parse_float(value) == expected


@pytest.mark.parametrize("value", [
    "nan",
    "Nan",
])
def test_parse_float_nan(value):
    assert isnan(parse_float(value))


def test_parse_str():
    value = "val"
    assert parse_str(value) == value


@pytest.mark.parametrize(("value", "expected"), [
    ("banana", ("banana",)),
    ("first, second", ("first", "second",))
])
def test_parse_tuple(value, expected):
    assert parse_tuple(value) == expected


@pytest.mark.parametrize(("value", "expected"), [
    ("banana", ("banana",)),
    ("first second", ("first", "second",))
])
def test_parse_tuple_with_seprator(value, expected):
    assert parse_tuple(value, separator=" ") == expected


@pytest.mark.parametrize(("value", "expected"), [
    ("42", (42,)),
    ("1, 2, 3", (1, 2, 3,))
])
def test_parse_tuple_with_subparser(value, expected):
    assert parse_tuple(value, subparser=parse_int) == expected
