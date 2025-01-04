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


class LazyEnvironment:
    """
    Provides lazy access to environment variables with support for parsing, prefixes,
    and deferred evaluation using `FutureValue`.

    This class supports retrieving environment variables with various data types
    and optional lazy evaluation of the parsed results.
    """

    def __init__(self, environ: Mapping[str, str] = os.environ, *, prefix: str = "") -> None:
        """
        Initialize the LazyEnvironment instance with the given environment mapping and prefix.

        :param environ: A mapping of environment variables (default is `os.environ`).
        :param prefix: An optional prefix to prepend to all variable names.
        """
        self._environ = environ
        self._prefix = prefix

    def __repr__(self) -> str:
        """
        Return a string representation of the LazyEnvironment instance.

        :return: A string representation showing the environment mapping.
        """
        return f"cabina.LazyEnvironment({self._environ!r})"

    def get(self, name: str, default: Union[NilType, ValueType] = Nil,
            parser: Callable[[str], ValueType] = parse_as_is) -> ValueType:
        """
        Retrieve an environment variable, applying a parser and handling defaults.

        :param name: The name of the environment variable (with prefix applied, if set).
        :param default: The default value to return if the variable is not found (default is `Nil`).
        :param parser: A callable to parse the variable's value (default is `parse_as_is`).
        :return: The parsed value of the environment variable or the default value.
        :raises EnvKeyError: If the variable is not found and no default value is provided.
        """
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
        """
        Retrieve an environment variable lazily, returning a `FutureValue`.

        The returned `FutureValue` object allows deferred evaluation of the parsed result.

        :param name: The name of the environment variable (with prefix applied, if set).
        :param default: The default value to return if the variable is not found (default is `Nil`).
        :param parser: A callable to parse the variable's value (default is `parse_as_is`).
        :return: A `FutureValue` instance for deferred evaluation of the environment variable.
        """
        kwargs: Dict[str, Any] = {}
        if default is not Nil:
            kwargs["default"] = default
        if parser is not parse_as_is:
            kwargs["parser"] = parser
        return cast(ValueType, FutureValue[ValueType](self.get, name, **kwargs))

    def __call__(self, name: str, default: Union[NilType, ValueType] = Nil,
                 parser: Callable[[str], ValueType] = parse_as_is) -> ValueType:
        """
        Retrieve an environment variable lazily by calling the instance as a function.

        This method is equivalent to calling `raw`.

        :param name: The name of the environment variable (with prefix applied, if set).
        :param default: The default value to return if the variable is not found (default is `Nil`).
        :param parser: A callable to parse the variable's value (default is `parse_as_is`).
        :return: A `FutureValue` instance for deferred evaluation of the environment variable.
        """
        return self.raw(name, default, parser)

    def none(self, name: str, default: Union[NilType, None] = Nil) -> None:
        """
        Retrieve an environment variable as a `None` type value lazily.

        :param name: The name of the environment variable (with prefix applied, if set).
        :param default: The default value to return if the variable is not found (default is `Nil`).
        :return: The parsed `None` value of the environment variable or the default value.
        """
        assert isinstance(default, (type(None), NilType))
        return self(name, default, parse_none)

    def bool(self, name: str, default: Union[NilType, bool] = Nil) -> bool:
        """
        Retrieve an environment variable as a boolean value lazily.

        :param name: The name of the environment variable (with prefix applied, if set).
        :param default: The default value to return if the variable is not found (default is `Nil`).
        :return: The parsed boolean value of the environment variable or the default value.
        """
        assert default is Nil or isinstance(default, bool)
        return self(name, default, parse_bool)

    def int(self, name: str, default: Union[NilType, int] = Nil) -> int:
        """
        Retrieve an environment variable as an integer value lazily.

        :param name: The name of the environment variable (with prefix applied, if set).
        :param default: The default value to return if the variable is not found (default is `Nil`).
        :return: The parsed integer value of the environment variable or the default value.
        """
        assert default is Nil or isinstance(default, int)
        return self(name, default, parse_int)

    def float(self, name: str, default: Union[NilType, float] = Nil) -> float:
        """
        Retrieve an environment variable as a floating-point value lazily.

        :param name: The name of the environment variable (with prefix applied, if set).
        :param default: The default value to return if the variable is not found (default is `Nil`).
        :return: The parsed float value of the environment variable or the default value.
        """
        assert default is Nil or isinstance(default, float)
        return self(name, default, parse_float)

    def tuple(self, name: str,
              default: Union[NilType, Tuple[ValueType, ...]] = Nil, *,
              separator: str = ",",
              subparser: Callable[[str], Any] = parse_str) -> Tuple[ValueType, ...]:
        """
        Retrieve an environment variable as a tuple of parsed values lazily.

        :param name: The name of the environment variable (with prefix applied, if set).
        :param default: The default value to return if the variable is not found (default is `Nil`).
        :param separator: The separator used to split the variable's value into elements.
        :param subparser: A callable to parse each element in the tuple (default is `parse_str`).
        :return: The parsed tuple value of the environment variable or the default value.
        """
        assert default is Nil or isinstance(default, tuple)
        parser = partial(parse_tuple, separator=separator, subparser=subparser)
        return self(name, default, parser)

    def str(self, name: str, default: Union[NilType, str] = Nil) -> str:
        """
        Retrieve an environment variable as a string value lazily.

        :param name: The name of the environment variable (with prefix applied, if set).
        :param default: The default value to return if the variable is not found (default is `Nil`).
        :return: A `FutureValue` instance for deferred evaluation of the string value.
        """
        assert default is Nil or isinstance(default, str)
        return self.raw(name, default, parse_str)
