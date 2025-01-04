from typing import Any, Callable

from ._core import MetaBase


def _required(*args: Any) -> Any:
    """
    Placeholder function for marking required arguments.

    This function is used internally to indicate a required argument
    when a default value is not provided.

    :param args: Placeholder arguments (unused).
    :return: None (function is a placeholder).
    """
    pass  # pragma: nocover


class computed:
    """
    Descriptor for defining computed properties on a class.

    This class provides a way to define properties that are computed dynamically
    based on a method. It is intended to be used as a decorator on a method.

    Example:
        @computed
        def some_property(cls):
            return cls.some_value * 2
    """

    def __init__(self, fn: Callable[[Any], Any] = _required) -> None:
        """
        Initialize the computed descriptor with the provided function.

        :param fn: The function to compute the property value.
        :raises TypeError: If the decorator is used incorrectly (e.g., `@computed()`).
        """
        if fn is _required:
            raise TypeError("Use @computed instead of @computed()")
        self._fn = fn

    def __get__(self, _: None, owner: MetaBase) -> Any:
        """
        Compute and return the value of the property.

        :param _: Unused; placeholder for the instance (as this is a class-level property).
        :param owner: The class (MetaBase) to which the computed property belongs.
        :return: The computed value of the property.
        """
        return self._fn(owner)
