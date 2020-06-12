import os
from typing import Any, Callable, Mapping, Union, cast

from niltype import Nil, NilType


def do_nothing(value: Any) -> Any:
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


def parse_int(value: str) -> int:
    return int(value)


def parse_float(value: str) -> float:
    return float(value)


def parse_str(value: str) -> str:
    return str(value)


class Environment:
    def __init__(self, environ: Mapping[str, str] = os.environ) -> None:
        self._environ = environ

    def __call__(self, name: str, default: Union[NilType, Any] = Nil, *,
                 parser: Any = do_nothing) -> Any:
        try:
            value = self._environ[name]
        except KeyError:
            if default is not Nil:
                return default
            raise
        else:
            return parser(value)

    def none(self, name: str, default: Union[NilType, None] = Nil, *,
             parser: Callable[[str], None] = parse_none) -> None:
        return cast(None,
                    self(name, default, parser=parser))

    def bool(self, name: str, default: Union[NilType, bool] = Nil, *,
             parser: Callable[[str], bool] = parse_bool) -> bool:
        return cast(bool,
                    self(name, default, parser=parser))

    def int(self, name: str, default: Union[NilType, int] = Nil, *,
            parser: Callable[[str], int] = parse_int) -> int:
        return cast(int,
                    self(name, default, parser=parser))

    def float(self, name: str, default: Union[NilType, float] = Nil, *,
              parser: Callable[[str], float] = parse_float) -> float:
        return cast(float,
                    self(name, default, parser=parser))

    def str(self, name: str, default: Union[NilType, str] = Nil, *,
            parser: Callable[[str], str] = parse_str) -> str:
        return cast(str,
                    self(name, default, parser=parser))
