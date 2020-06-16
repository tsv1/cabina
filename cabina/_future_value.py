from typing import Any, Callable, Generic, TypeVar, Union

from niltype import Nil, NilType

ValueType = TypeVar("ValueType")


class FutureValue(Generic[ValueType]):
    def __init__(self, accessor: Callable[..., ValueType], *args: Any, **kwargs: Any) -> None:
        self._accessor = accessor
        self._args = args
        self._kwargs = kwargs
        self._value: Union[ValueType, NilType] = Nil

    def fetch(self) -> ValueType:
        self._value = self._accessor(*self._args, **self._kwargs)
        return self._value

    def get(self) -> ValueType:
        if self._value is Nil:
            return self.fetch()
        return self._value
