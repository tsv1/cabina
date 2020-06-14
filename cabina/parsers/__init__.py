from typing import Any, Callable, Tuple

__all__ = ("parse_as_is", "parse_none", "parse_bool", "parse_int",
           "parse_float", "parse_str", "parse_tuple",)


class ParseError(TypeError):
    pass


def parse_as_is(value: Any) -> Any:
    return value


def parse_none(value: str) -> None:
    if value.lower() in ("none", "null", "nil",):
        return None
    raise ParseError(f"Failed to parse {value!r} as None")


def parse_bool(value: str) -> bool:
    if value.lower() in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif value.lower() in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ParseError(f"Failed to parse {value!r} as bool")


def parse_int(value: str, *, base: int = 10) -> int:
    try:
        return int(value, base)
    except ValueError:
        if base == 10:
            raise ParseError(f"Failed to parse {value!r} as int")
        raise ParseError(f"Failed to parse {value!r} as int with base {base}")


def parse_float(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        raise ParseError(f"Failed to parse {value!r} as float")


def parse_str(value: str, *,
              not_empty: bool = True,
              trim: Callable[[str], str] = str.strip) -> str:
    parsed = trim(value)
    if not_empty and parsed == "":
        raise ParseError(f"Failed to parse {value!r} as non-empty str")
    return parsed


def parse_tuple(value: str, *, separator: str = ",",
                subparser: Callable[[str], Any] = parse_str) -> Tuple[Any, ...]:
    parsed = value.split(separator)
    try:
        return tuple(subparser(x) for x in parsed)
    except ParseError as e:
        raise ParseError(f"Failed to parse {value!r} as tuple: {e}")
