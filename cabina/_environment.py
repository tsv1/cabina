import os
from functools import partial
from typing import Any, Mapping, Tuple, Union, cast

from niltype import Nil, NilType

from ._parsers import (
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

    def __call__(self, name: str, default: Union[NilType, Any] = Nil,
                 parser: Any = parse_as_is) -> Any:
        try:
            value = self._environ[name]
        except KeyError:
            if default is not Nil:
                return default
            raise
        else:
            return parser(value)

    def none(self, name: str, default: Union[NilType, None] = Nil) -> None:
        return cast(None, self(name, default, parser=parse_none))

    def bool(self, name: str, default: Union[NilType, bool] = Nil) -> bool:
        return cast(bool, self(name, default, parser=parse_bool))

    def int(self, name: str, default: Union[NilType, int] = Nil) -> int:
        return cast(int, self(name, default, parser=parse_int))

    def float(self, name: str, default: Union[NilType, float] = Nil) -> float:
        return cast(float, self(name, default, parser=parse_float))

    def tuple(self, name: str, default: Union[NilType, str] = Nil, *,
              separator: str = ",") -> Tuple[str, ...]:
        parser = partial(parse_tuple, separator=separator)
        return cast(Tuple[str, ...], self(name, default, parser=parser))

    def str(self, name: str, default: Union[NilType, str] = Nil) -> str:
        return cast(str, self(name, default, parser=parse_str))
