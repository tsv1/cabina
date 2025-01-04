from typing import Any, Callable, Tuple

from ..errors import EnvParseError

__all__ = (
    "parse_as_is",
    "parse_none",
    "parse_bool",
    "parse_int",
    "parse_float",
    "parse_str",
    "parse_tuple",
)


def parse_as_is(value: Any) -> Any:
    """
    Return the value as is without any parsing.

    :param value: The value to return as is.
    :return: The same value without modification.
    """
    return value


def parse_none(value: str) -> None:
    """
    Parse a string as `None` if it matches specific null-like values.

    Valid null-like values are "none", "null", or "nil" (case-insensitive).

    :param value: The string to parse.
    :return: `None` if the value matches a null-like string.
    :raises EnvParseError: If the value does not match any null-like string.
    """
    if value.lower() in ("none", "null", "nil"):
        return None
    raise EnvParseError(f"Failed to parse {value!r} as None")


def parse_bool(value: str) -> bool:
    """
    Parse a string as a boolean value.

    Valid true-like values: "y", "yes", "t", "true", "on", "1" (case-insensitive).
    Valid false-like values: "n", "no", "f", "false", "off", "0" (case-insensitive).

    :param value: The string to parse.
    :return: `True` if the value matches a true-like string, `False` otherwise.
    :raises EnvParseError: If the value does not match any boolean-like string.
    """
    if value.lower() in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif value.lower() in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise EnvParseError(f"Failed to parse {value!r} as bool")


def parse_int(value: str, *, base: int = 10) -> int:
    """
    Parse a string as an integer.

    :param value: The string to parse.
    :param base: The numeric base to use for parsing (default is 10).
    :return: The parsed integer.
    :raises EnvParseError: If the value cannot be parsed as an integer.
    """
    try:
        return int(value, base)
    except ValueError:
        if base == 10:
            raise EnvParseError(f"Failed to parse {value!r} as int") from None
        raise EnvParseError(f"Failed to parse {value!r} as int with base {base}") from None


def parse_float(value: str) -> float:
    """
    Parse a string as a floating-point number.

    :param value: The string to parse.
    :return: The parsed float.
    :raises EnvParseError: If the value cannot be parsed as a float.
    """
    try:
        return float(value)
    except ValueError:
        raise EnvParseError(f"Failed to parse {value!r} as float") from None


def parse_str(value: str, *,
              not_empty: bool = True,
              trim: Callable[[str], str] = str.strip) -> str:
    """
    Parse a string, optionally enforcing non-emptiness and applying trimming.

    :param value: The string to parse.
    :param not_empty: Whether to enforce that the parsed string is not empty (default is True).
    :param trim: A callable to apply trimming to the string (default is `str.strip`).
    :return: The parsed string.
    :raises EnvParseError: If the string is empty and `not_empty` is True.
    """
    parsed = trim(value)
    if not_empty and parsed == "":
        raise EnvParseError(f"Failed to parse {value!r} as non-empty str")
    return parsed


def parse_tuple(value: str, *, separator: str = ",",
                subparser: Callable[[str], Any] = parse_str) -> Tuple[Any, ...]:
    """
    Parse a string as a tuple, splitting by a separator and applying a subparser.

    The string may optionally be enclosed in parentheses.

    :param value: The string to parse.
    :param separator: The separator to use for splitting the string into elements (default is ",").
    :param subparser: A callable to parse each element in the tuple (default is `parse_str`).
    :return: The parsed tuple.
    :raises EnvParseError: If parsing any element fails or if the string format is invalid.
    """
    if value.startswith("(") and value.endswith(")"):
        value = value[1:-1]
    if value.endswith(separator):
        value = value[:-len(separator)]
    parsed = value.split(separator)
    try:
        return tuple(subparser(x) for x in parsed)
    except EnvParseError as e:
        raise EnvParseError(f"Failed to parse {value!r} as tuple: {e}") from None
