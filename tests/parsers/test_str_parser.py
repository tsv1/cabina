import pytest
from pytest import raises

from cabina.errors import EnvParseError
from cabina.parsers import parse_str


@pytest.mark.parametrize("value", [
    "banana",
    " banana",
    "banana ",
    " banana ",
    "  banana  ",
])
def test_parse_str(value):
    assert parse_str(value) == "banana"


def test_parse_empty_str():
    with raises(Exception) as exc_info:
        parse_str("")

    assert exc_info.type is EnvParseError
    assert str(exc_info.value) == "Failed to parse '' as non-empty str"
