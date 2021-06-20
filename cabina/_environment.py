import os
from functools import partial
from typing import Any, Callable, Dict, Mapping, Tuple, Union, cast

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
    def __init__(self, environ: Mapping[str, str] = os.environ, *, prefix: str = "") -> None:
        self._environ = environ
        self._prefix = prefix

    def __repr__(self) -> str:
        return f"cabina.Environment({self._environ!r})"

    def get(self, name: str, default: Union[NilType, ValueType] = Nil,
            parser: Callable[[str], ValueType] = parse_as_is) -> ValueType:
        if self._prefix:
            name = self._prefix + name
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
        kwargs: Dict[str, Any] = {}
        if default is not Nil:
            kwargs["default"] = default
        if parser is not parse_as_is:
            kwargs["parser"] = parser
        return cast(ValueType, FutureValue[ValueType](self.get, name, **kwargs))

    def __call__(self, name: str, default: Union[NilType, ValueType] = Nil,
                 parser: Callable[[str], ValueType] = parse_as_is) -> ValueType:
        return self.raw(name, default, parser)

    def none(self, name: str, default: Union[NilType, None] = Nil) -> None:
        assert isinstance(default, (type(None), NilType))
        return self(name, default, parse_none)

    def bool(self, name: str, default: Union[NilType, bool] = Nil) -> bool:
        assert default is Nil or isinstance(default, bool)
        return self(name, default, parse_bool)

    def int(self, name: str, default: Union[NilType, int] = Nil) -> int:
        assert default is Nil or isinstance(default, int)
        return self(name, default, parse_int)

    def float(self, name: str, default: Union[NilType, float] = Nil) -> float:
        assert default is Nil or isinstance(default, float)
        return self(name, default, parse_float)

    def tuple(self, name: str,
              default: Union[NilType, Tuple[ValueType, ...]] = Nil, *,
              separator: str = ",",
              subparser: Callable[[str], Any] = parse_str) -> Tuple[ValueType, ...]:
        assert default is Nil or isinstance(default, tuple)
        parser = partial(parse_tuple, separator=separator, subparser=subparser)
        return self(name, default, parser)

    def str(self, name: str, default: Union[NilType, str] = Nil) -> str:
        assert default is Nil or isinstance(default, str)
        return self.raw(name, default, parse_str)
