import inspect
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
                    raise ConfigError(f"Attempted to add non-Section {key!r} to {cls!r}")
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
        raise ConfigAttrError(f"{name!r} does not exist in {cls!r}")

    def __setattr__(cls, name: str, value: Any) -> None:
        if cls.__frozen__ and name != "__frozen__":
            if name in cls:
                raise ConfigError(f"Attempted to override {name!r} in {cls!r}")
            raise ConfigError(f"Attempted to add {name!r} to {cls!r} at runtime")
        super().__setattr__(name, value)

    def __delattr__(cls, name: str) -> None:
        raise ConfigError(f"Attempted to remove {name!r} from {cls!r}")

    def __getitem__(cls, key: str) -> Any:
        if key in cls:
            return getattr(cls, key)
        raise ConfigKeyError(f"{key!r} does not exist in {cls!r}")

    def __setitem__(cls, key: str, value: Any) -> None:
        return setattr(cls, key, value)

    def __delitem__(cls, key: str) -> None:
        return delattr(cls, key)

    def __call__(cls, *args: Any, **kwargs: Any) -> None:
        if _is_config(cls):
            raise ConfigError(f"Attempted to initialize config {cls!r}")
        elif _is_section(cls):
            raise ConfigError(f"Attempted to initialize section {cls!r}")
        else:  # pragma: nocover
            pass

    def __len__(cls) -> int:
        return len(cls.__members__)

    def __iter__(cls) -> Iterator[str]:
        return cls.__members__.__iter__()

    def __contains__(cls, item: Any) -> bool:
        return item in cls.__members__

    def __repr__(cls) -> str:
        namespace = [cls.__name__]
        parent = cls.__parent__
        while parent is not None:
            namespace += [parent.__name__]
            parent = parent.__parent__
        return "<" + ".".join(reversed(namespace)) + ">"

    def keys(cls) -> KeysView[str]:
        return cls.__members__.keys()

    def values(cls) -> ValuesView[Any]:
        return {key: getattr(cls, key) for key in cls.__members__}.values()

    def items(cls) -> ItemsView[str, Any]:
        return {key: getattr(cls, key) for key in cls.__members__}.items()

    def get(cls, key: str, default: Union[NilType, Any] = Nil) -> Any:
        try:
            return cls[key]
        except KeyError:
            if default is not Nil:
                return default
            raise

    def __prefetch(cls) -> List[str]:
        errors: List[str] = []
        for key in cls.__members__:
            try:
                val = getattr(cls, key)
            except (EnvKeyError, EnvParseError) as e:
                namespace = repr(cls)[1:-1]
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
