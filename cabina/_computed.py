from typing import Any, Callable

from ._core import MetaBase


class computed:
    def __init__(self, fn: Callable[[MetaBase], Any]) -> None:
        self._fn = fn

    def __get__(self, _: None, owner: MetaBase) -> Any:
        return self._fn(owner)
