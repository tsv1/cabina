import pytest
from pytest import raises

from cabina.errors import EnvParseError
from cabina.parsers import parse_int, parse_tuple


@pytest.mark.parametrize(("value", "expected"), [
    ("banana", ("banana",)),
    ("banana,", ("banana",)),
    ("(banana)", ("banana",)),
    ("(banana,)", ("banana",)),
    ("first, second", ("first", "second",)),
    ("first, second,", ("first", "second",)),
    ("(first, second)", ("first", "second",)),
    ("(first, second,)", ("first", "second",)),
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


def test_parse_empty_tuple():
    with raises(Exception) as exc_info:
        parse_tuple("")

    assert exc_info.type is EnvParseError
    assert str(exc_info.value) == ("Failed to parse '' as tuple: "
                                   "Failed to parse '' as non-empty str")


def test_parse_invalid_tuple():
    with raises(Exception) as exc_info:
        parse_tuple("banana,,")

    assert exc_info.type is EnvParseError
    assert str(exc_info.value) == ("Failed to parse 'banana,' as tuple: "
                                   "Failed to parse '' as non-empty str")
