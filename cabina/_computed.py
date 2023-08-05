from typing import Any, Callable

from ._core import MetaBase
from .errors import ConfigError, Error


def _required(*args: Any) -> Any:
    pass  # pragma: nocover


class computed:
    def __init__(self, fn: Callable[[Any], Any] = _required) -> None:
        if fn is _required:
            raise TypeError("Use @computed instead of @computed()")
        self._fn = fn

    def __get__(self, _: None, owner: MetaBase) -> Any:
        try:
            return self._fn(owner)
        except Error as e:
            raise ConfigError(f"Failed to return @computed '{self._fn.__name__}' ({e})") from None
