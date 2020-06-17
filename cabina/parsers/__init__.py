from typing import Any, Callable, Tuple

from ..errors import EnvParseError

__all__ = ("parse_as_is", "parse_none", "parse_bool", "parse_int",
           "parse_float", "parse_str", "parse_tuple",)


def parse_as_is(value: Any) -> Any:
    return value


def parse_none(value: str) -> None:
    if value.lower() in ("none", "null", "nil",):
        return None
    raise EnvParseError(f"Failed to parse {value!r} as None")


def parse_bool(value: str) -> bool:
    if value.lower() in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif value.lower() in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise EnvParseError(f"Failed to parse {value!r} as bool")


def parse_int(value: str, *, base: int = 10) -> int:
    try:
        return int(value, base)
    except ValueError:
        if base == 10:
            raise EnvParseError(f"Failed to parse {value!r} as int") from None
        raise EnvParseError(f"Failed to parse {value!r} as int with base {base}") from None


def parse_float(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        raise EnvParseError(f"Failed to parse {value!r} as float") from None


def parse_str(value: str, *,
              not_empty: bool = True,
              trim: Callable[[str], str] = str.strip) -> str:
    parsed = trim(value)
    if not_empty and parsed == "":
        raise EnvParseError(f"Failed to parse {value!r} as non-empty str")
    return parsed


def parse_tuple(value: str, *, separator: str = ",",
                subparser: Callable[[str], Any] = parse_str) -> Tuple[Any, ...]:
    if value.startswith("(") and value.endswith(")"):
        value = value[1:-1]
    if value.endswith(separator):
        value = value[:-len(separator)]
    parsed = value.split(separator)
    try:
        return tuple(subparser(x) for x in parsed)
    except EnvParseError as e:
        raise EnvParseError(f"Failed to parse {value!r} as tuple: {e}") from None
