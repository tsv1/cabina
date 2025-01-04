from typing import Any, Callable, Generic, TypeVar, Union

from niltype import Nil, NilType

ValueType = TypeVar("ValueType")


class FutureValue(Generic[ValueType]):
    """
    Represents a lazily-evaluated value that is computed only when needed.

    This class allows the deferred computation of a value using a provided accessor function.
    The value is cached after the first computation and reused for subsequent accesses.
    """

    def __init__(self, accessor: Callable[..., ValueType], *args: Any, **kwargs: Any) -> None:
        """
        Initialize the FutureValue with an accessor function and optional arguments.

        :param accessor: The function used to compute the value when needed.
        :param args: Positional arguments to pass to the accessor function.
        :param kwargs: Keyword arguments to pass to the accessor function.
        """
        self._accessor = accessor
        self._args = args
        self._kwargs = kwargs
        self._value: Union[ValueType, NilType] = Nil

    def fetch(self) -> ValueType:
        """
        Compute the value by calling the accessor function.

        This method directly evaluates the value and updates the internal cache.

        :return: The computed value.
        """
        self._value = self._accessor(*self._args, **self._kwargs)
        return self._value

    def get(self) -> ValueType:
        """
        Retrieve the value, computing it if necessary.

        If the value has already been computed, the cached value is returned.
        Otherwise, the accessor function is called to compute and cache the value.

        :return: The computed or cached value.
        """
        if self._value is Nil:
            return self.fetch()
        return self._value

    def __repr__(self) -> str:
        """
        Get a string representation of the FutureValue instance.

        The representation includes the accessor arguments (if any) and keyword arguments.

        :return: A string representation of the FutureValue instance.
        """
        args = [repr(arg) for arg in self._args]
        str_args = ", ".join(args)

        kwargs = [f"{key}={val!r}" for key, val in self._kwargs.items()]
        str_kwargs = ", ".join(kwargs)

        if (len(args) > 0) and (len(kwargs) > 0):
            return f"FutureValue({str_args}, {str_kwargs})"
        elif len(args) > 0:
            return f"FutureValue({str_args})"
        return f"FutureValue({str_kwargs})"
