import pytest

from cabina.parsers import parse_as_is


@pytest.mark.parametrize("value", [
    "",
    "None",
    "True",
    "42",
    "3.14",
    "banana",
])
def test_parse_as_is(value):
    assert parse_as_is(value) == value
