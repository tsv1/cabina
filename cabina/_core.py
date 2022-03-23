import inspect
import sys
import warnings
from typing import (
    Any,
    Dict,
    ItemsView,
    Iterator,
    KeysView,
    List,
    Optional,
    Tuple,
    Union,
    ValuesView,
)

from niltype import Nil, NilType

from ._future_value import FutureValue
from .errors import (
    ConfigAttrError,
    ConfigEnvError,
    ConfigError,
    ConfigKeyError,
    EnvKeyError,
    EnvParseError,
)

_Section = None
_Config = None


def _is_dunder(name: str) -> bool:
    return (name[:2] == name[-2:] == '__' and
            name[2:3] != '_' and
            name[-3:-2] != '_' and
            len(name) > 4)


def _is_section(cls: Any) -> bool:
    return _Section is not None and issubclass(cls, _Section)


def _is_config(cls: Any) -> bool:
    return _Config is not None and issubclass(cls, _Config)


def _is_subclass(cls: Any, cls_type: Any) -> bool:
    return inspect.isclass(cls) and issubclass(cls, cls_type)


class UniqueDict(Dict[str, Any]):
    def __init__(self, namespace: str) -> None:
        super().__init__()
        self.__namespace = namespace

    def __setitem__(self, key: str, value: Any) -> None:
        if not _is_dunder(key) and key in self:
            raise ConfigError(f"Attempted to reuse {key!r} in {self.__namespace!r}")
        super().__setitem__(key, value)


class MetaBase(type):
    @classmethod
    def __prepare__(mcs, name: str, bases: Tuple[Any]) -> UniqueDict:  # type: ignore
        return UniqueDict(name)

    def __init__(cls, name: str, bases: Tuple[Any], attrs: Dict[str, Any]) -> None:
        super().__init__(name, bases, attrs)

        for base in bases:
            if not _is_subclass(base, (_Config, _Section)):
                raise ConfigError(f"Attempted to inherit {base!r}")

        if _is_config(cls) or _is_section(cls):
            cls.__frozen__ = False
            cls.__members__ = {}

        reserved = set(dir(cls.__class__))
        for key, val in attrs.items():
            if _is_dunder(key):
                continue

            if key in reserved:
                raise ConfigError(f"Attempted to use reserved {key!r} in {name!r}")

            if _is_subclass(val, _Section):
                val.__frozen__ = False
                val.__parent__ = cls
                val.__frozen__ = True

            if _is_config(cls) and _is_section(cls):
                cls.__members__[key] = val
            elif _is_section(cls):
                cls.__members__[key] = val
            elif _is_config(cls):
                if not _is_subclass(val, _Section):
                    name = cls.__get_full_name()
                    raise ConfigError(f"Attempted to add non-Section {key!r} to <{name}>")
                cls.__members__[key] = val
            else:  # pragma: no cover
                pass

        if _is_config(cls) or _is_section(cls):
            cls.__frozen__ = True

    def __getattribute__(cls, name: str) -> Any:
        attr = super().__getattribute__(name)
        if isinstance(attr, FutureValue):
            return attr.get()
        return attr

    def __getattr__(cls, name: str) -> Any:
        raise ConfigAttrError(f"{name!r} does not exist in <{cls.__get_full_name()}>")

    def __setattr__(cls, name: str, value: Any) -> None:
        if cls.__frozen__ and name != "__frozen__":
            if name in cls:
                raise ConfigError(f"Attempted to override {name!r} in <{cls.__get_full_name()}>")
            raise ConfigError(f"Attempted to add {name!r} to <{cls.__get_full_name()}> at runtime")
        super().__setattr__(name, value)

    def __delattr__(cls, name: str) -> None:
        raise ConfigError(f"Attempted to remove {name!r} from <{cls.__get_full_name()}>")

    def __getitem__(cls, key: str) -> Any:
        if key in cls:
            return getattr(cls, key)
        raise ConfigKeyError(f"{key!r} does not exist in <{cls.__get_full_name()}>")

    def __setitem__(cls, key: str, value: Any) -> None:
        return setattr(cls, key, value)

    def __delitem__(cls, key: str) -> None:
        return delattr(cls, key)

    def __call__(cls, *args: Any, **kwargs: Any) -> None:
        if _is_config(cls):
            raise ConfigError(f"Attempted to initialize config <{cls.__get_full_name()}>")
        elif _is_section(cls):
            raise ConfigError(f"Attempted to initialize section <{cls.__get_full_name()}>")
        else:  # pragma: nocover
            pass

    @property
    def __members(cls) -> Dict[str, Any]:
        result = {}

        for base in reversed(cls.__bases__):
            if _is_config(base) or _is_section(base):
                for key in base:  # type: ignore
                    result[key] = ...

        for key in cls.__members__:
            result[key] = ...

        return result

    def __len__(cls) -> int:
        return len(cls.__members)

    def __iter__(cls) -> Iterator[str]:
        return cls.__members.__iter__()

    def __contains__(cls, item: Any) -> bool:
        return item in cls.__members

    def __repr__(cls) -> str:
        formatted = cls.__format(name=cls.__get_full_name())
        return "\n".join(formatted)

    def __get_full_name(cls) -> str:
        namespace = [cls.__name__]
        parent = cls.__parent__
        while parent is not None:
            namespace += [parent.__name__]
            parent = parent.__parent__
        return ".".join(reversed(namespace))

    def keys(cls) -> KeysView[str]:
        return cls.__members.keys()

    def values(cls) -> ValuesView[Any]:
        return {key: val for key, val in cls.items()}.values()

    def items(cls) -> ItemsView[str, Any]:
        items = {}
        for key in cls.__members:
            try:
                items[key] = getattr(cls, key)
            except Exception as e:
                items[key] = e
        return items.items()

    def get(cls, key: str, default: Union[NilType, Any] = Nil) -> Any:
        try:
            return cls[key]
        except KeyError:
            if default is not Nil:
                return default
            raise

    def __prefetch(cls) -> List[str]:
        errors: List[str] = []
        for key in cls.__members:
            try:
                val = getattr(cls, key)
            except (EnvKeyError, EnvParseError) as e:
                namespace = cls.__get_full_name()
                message = f"{namespace}.{key}: {e}"
                errors.append(message)
            else:
                if _is_subclass(val, _Section):
                    errors += val.__prefetch()
        return errors

    def prefetch(cls) -> None:
        errors = cls.__prefetch()
        if len(errors) > 0:
            prefix = "\n- "
            message = f"Failed to prefetch:{prefix}" + prefix.join(errors)
            raise ConfigEnvError(message)

    def __format(cls, *,
                 indent: int = 0, prepend: bool = False, name: Optional[str] = None) -> List[str]:
        res = [""] if prepend else []

        name = name or cls.__name__
        res.append(" " * indent + f"class <{name}>:")
        if len(cls) > 0:
            for key, val in cls.items():
                if _is_subclass(val, (_Config, _Section)):
                    res += val.__format(indent=indent + 4, prepend=True)
                else:
                    res.append(" " * (indent + 4) + f"{key} = {val!r}")
        else:
            res.append(" " * (indent + 4) + "...")

        return res

    def print(cls, stream: Any = sys.stdout) -> None:
        warnings.warn("Deprecated: use print(<cls>) instead", DeprecationWarning)
        formatted = "\n".join(cls.__format())
        print(formatted, file=stream)


class Section(metaclass=MetaBase):
    __frozen__: bool = False
    __parent__: Optional[MetaBase] = None
    __members__: Dict[str, Any] = {}


_Section = Section


class Config(metaclass=MetaBase):
    __frozen__: bool = False
    __parent__: Optional[MetaBase] = None
    __members__:  Dict[str, Any] = {}


_Config = Config
