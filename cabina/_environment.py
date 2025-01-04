import os
from functools import partial
from typing import Any, Callable, Mapping, Tuple, Union

from niltype import Nil, NilType

from ._future_value import ValueType
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
    """
    Provides access to environment variables with parsing and optional prefixes.

    This class supports retrieving environment variables with various data types,
    applying parsers for conversion, and handling default values for missing keys.
    """

    def __init__(self, environ: Mapping[str, str] = os.environ, *, prefix: str = "") -> None:
        """
        Initialize the Environment instance with the given environment mapping and prefix.

        :param environ: A mapping of environment variables (default is `os.environ`).
        :param prefix: An optional prefix to prepend to all variable names.
        """
        self._environ = environ
        self._prefix = prefix

    def __repr__(self) -> str:
        """
        Return a string representation of the Environment instance.

        :return: A string representation showing the environment mapping.
        """
        return f"cabina.Environment({self._environ!r})"

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
        Retrieve an environment variable as is, without applying additional logic.

        This method is equivalent to `get`.

        :param name: The name of the environment variable (with prefix applied, if set).
        :param default: The default value to return if the variable is not found (default is `Nil`).
        :param parser: A callable to parse the variable's value (default is `parse_as_is`).
        :return: The parsed value of the environment variable or the default value.
        """
        return self.get(name, default, parser)

    def __call__(self, name: str, default: Union[NilType, ValueType] = Nil,
                 parser: Callable[[str], ValueType] = parse_as_is) -> ValueType:
        """
        Retrieve an environment variable by calling the instance as a function.

        :param name: The name of the environment variable (with prefix applied, if set).
        :param default: The default value to return if the variable is not found (default is `Nil`).
        :param parser: A callable to parse the variable's value (default is `parse_as_is`).
        :return: The parsed value of the environment variable or the default value.
        """
        return self.raw(name, default, parser)

    def none(self, name: str, default: Union[NilType, None] = Nil) -> None:
        """
        Retrieve an environment variable as a `None` type value.

        :param name: The name of the environment variable (with prefix applied, if set).
        :param default: The default value to return if the variable is not found (default is `Nil`).
        :return: The parsed `None` value of the environment variable or the default value.
        """
        assert isinstance(default, (type(None), NilType))
        return self(name, default, parse_none)

    def bool(self, name: str, default: Union[NilType, bool] = Nil) -> bool:
        """
        Retrieve an environment variable as a boolean value.

        :param name: The name of the environment variable (with prefix applied, if set).
        :param default: The default value to return if the variable is not found (default is `Nil`).
        :return: The parsed boolean value of the environment variable or the default value.
        """
        assert default is Nil or isinstance(default, bool)
        return self(name, default, parse_bool)

    def int(self, name: str, default: Union[NilType, int] = Nil) -> int:
        """
        Retrieve an environment variable as an integer value.

        :param name: The name of the environment variable (with prefix applied, if set).
        :param default: The default value to return if the variable is not found (default is `Nil`).
        :return: The parsed integer value of the environment variable or the default value.
        """
        assert default is Nil or isinstance(default, int)
        return self(name, default, parse_int)

    def float(self, name: str, default: Union[NilType, float] = Nil) -> float:
        """
        Retrieve an environment variable as a floating-point value.

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
        Retrieve an environment variable as a tuple of parsed values.

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
        Retrieve an environment variable as a string value.

        :param name: The name of the environment variable (with prefix applied, if set).
        :param default: The default value to return if the variable is not found (default is `Nil`).
        :return: The parsed string value of the environment variable or the default value.
        """
        assert default is Nil or isinstance(default, str)
        return self.raw(name, default, parse_str)
