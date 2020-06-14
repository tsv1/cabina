from typing import Any, Callable, Tuple


def parse_as_is(value: Any) -> Any:
    return value


def parse_none(value: str) -> None:
    if value.lower() in ("none", "null", "nil",):
        return None
    raise ValueError(value)


def parse_bool(value: str) -> bool:
    if value.lower() in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif value.lower() in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ValueError(value)


def parse_int(value: str, *, base: int = 10) -> int:
    return int(value, base)


def parse_float(value: str) -> float:
    return float(value)


def parse_str(value: str, *,
              not_empty: bool = True,
              trim: Callable[[str], str] = str.strip) -> str:
    parsed = trim(value)
    if not_empty and parsed == "":
        raise ValueError(value)
    return parsed


def parse_tuple(value: str, *, separator: str = ",",
                subparser: Callable[[str], Any] = parse_str) -> Tuple[Any, ...]:
    parsed = value.split(separator)
    return tuple(subparser(x) for x in parsed)
