import inspect
from typing import Any, Dict, ItemsView, Iterator, KeysView, Tuple, ValuesView


def _is_dunder(name: str) -> bool:
    return (name[:2] == name[-2:] == '__' and
            name[2:3] != '_' and
            name[-3:-2] != '_' and
            len(name) > 4)


_Section = None
_Config = None


def _is_section(cls: Any) -> bool:
    return _Section is not None and issubclass(cls, _Section)


def _is_config(cls: Any) -> bool:
    return _Config is not None and issubclass(cls, _Config)


class MetaBase(type):
    def __init__(cls, name: str, bases: Tuple[Any], attrs: Dict[Any, Any]) -> None:
        super().__init__(name, bases, attrs)

        if _is_config(cls) or _is_section(cls):
            cls.__members__ = {}

        for key, val in attrs.items():
            if _is_dunder(key):
                continue

            if _is_config(cls) and _is_section(cls):
                cls.__members__[key] = val
            elif _is_section(cls):
                cls.__members__[key] = val
            elif _is_config(cls):
                if not inspect.isclass(val) or not issubclass(val, _Section):  # type: ignore
                    raise TypeError(f"isclass {val!r}")
                cls.__members__[key] = val
            else:  # pragma: no cover
                pass

        if _is_config(cls) or _is_section(cls):
            cls.__frozen__ = True

    def __setattr__(cls, name: Any, value: Any) -> None:
        if cls.__frozen__:
            raise TypeError(f"__setattr__ {name}")
        super().__setattr__(name, value)

    def __delattr__(cls, name: Any) -> None:
        raise TypeError(f"__delattr__ {name}")

    def __getitem__(cls, item: Any) -> Any:
        return getattr(cls, item)

    def __setitem__(cls, key: Any, value: Any) -> None:
        raise TypeError(f"__setitem__ {key}")

    def __delitem__(cls, key: Any) -> None:
        raise TypeError(f"__delitem__ {key}")

    def __call__(cls, *args: Any, **kwargs: Any) -> None:
        raise TypeError("__init__")

    def __len__(cls) -> int:
        return len(cls.__members__)

    def __iter__(cls) -> Iterator[Any]:
        return cls.__members__.__iter__()

    def __contains__(cls, item: Any) -> bool:
        return item in cls.__members__

    def keys(cls) -> KeysView[Any]:
        return cls.__members__.keys()

    def values(cls) -> ValuesView[Any]:
        return cls.__members__.values()

    def items(cls) -> ItemsView[Any, Any]:
        return cls.__members__.items()


class Section(metaclass=MetaBase):
    __frozen__ = False
    __members__: Dict[Any, Any] = {}


_Section = Section


class Config(metaclass=MetaBase):
    __frozen__ = False
    __members__:  Dict[Any, Any] = {}


_Config = Config
