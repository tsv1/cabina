import os
from functools import partial
from typing import Callable, Mapping, Tuple, Union, cast

from niltype import Nil, NilType

from ._future_value import FutureValue, ValueType
from .errors import EnvKeyError
from .parsers import (
    parse_as_is,
    parse_bool,
    parse_float,
    parse_int,
    parse_none,
    parse_str,
    parse_tuple,
)


class Environment:
    def __init__(self, environ: Mapping[str, str] = os.environ) -> None:
        self._environ = environ

    def __repr__(self) -> str:
        return f"cabina.Environment({self._environ!r})"

    def get(self, name: str, default: Union[NilType, ValueType] = Nil,
            parser: Callable[[str], ValueType] = parse_as_is) -> ValueType:
        try:
            value = self._environ[name]
        except KeyError:
            if default is Nil:
                raise EnvKeyError(f"{name!r} does not exist") from None
            return default
        else:
            return parser(value)

    def raw(self, name: str, default: Union[NilType, ValueType] = Nil,
            parser: Callable[[str], ValueType] = parse_as_is) -> ValueType:
        return cast(ValueType, FutureValue[ValueType](self.get, name, default, parser))

    def __call__(self, name: str, default: Union[NilType, ValueType] = Nil,
                 parser: Callable[[str], ValueType] = parse_as_is) -> ValueType:
        return self.raw(name, default, parser)

    def none(self, name: str, default: Union[NilType, None] = Nil) -> None:
        return self(name, default, parse_none)

    def bool(self, name: str, default: Union[NilType, bool] = Nil) -> bool:
        return self(name, default, parse_bool)

    def int(self, name: str, default: Union[NilType, int] = Nil) -> int:
        return self(name, default, parse_int)

    def float(self, name: str, default: Union[NilType, float] = Nil) -> float:
        return self(name, default, parse_float)

    def tuple(self, name: str, default: Union[NilType, str] = Nil, *,
              separator: str = ",") -> Tuple[str, ...]:
        parser = partial(parse_tuple, separator=separator)
        return self(name, default, parser)

    def str(self, name: str, default: Union[NilType, str] = Nil) -> str:
        return self.raw(name, default, parse_str)
