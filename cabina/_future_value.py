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

    def __repr__(self) -> str:
        args = [repr(arg) for arg in self._args]
        str_args = ", ".join(args)

        kwargs = [f"{key}={val!r}" for key, val in self._kwargs.items()]
        str_kwargs = ", ".join(kwargs)

        if (len(args) > 0) and (len(kwargs) > 0):
            return f"FutureValue({str_args}, {str_kwargs})"
        elif len(args) > 0:
            return f"FutureValue({str_args})"
        return f"FutureValue({str_kwargs})"
