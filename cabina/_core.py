import inspect
import os
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
    """
    Check if a given name is a dunder (double underscore) name.

    :param name: The name to check.
    :return: True if the name is a dunder name, False otherwise.
    """
    return (name[:2] == name[-2:] == '__' and
            name[2:3] != '_' and
            name[-3:-2] != '_' and
            len(name) > 4)


def _is_section(cls: Any) -> bool:
    """
    Check if a given class is a subclass of _Section.

    :param cls: The class to check.
    :return: True if the class is a subclass of _Section, False otherwise.
    """
    return _Section is not None and issubclass(cls, _Section)


def _is_config(cls: Any) -> bool:
    """
    Check if a given class is a subclass of _Config.

    :param cls: The class to check.
    :return: True if the class is a subclass of _Config, False otherwise.
    """
    return _Config is not None and issubclass(cls, _Config)


def _is_subclass(cls: Any, cls_type: Any) -> bool:
    """
    Check if a given class is a subclass of a specified type.

    :param cls: The class to check.
    :param cls_type: The type to check against.
    :return: True if the class is a subclass of the specified type, False otherwise.
    """
    return inspect.isclass(cls) and issubclass(cls, cls_type)


class UniqueDict(Dict[str, Any]):
    """
    Represents a dictionary that enforces unique keys within a specified namespace.

    This dictionary raises an error if a non-dunder key is reused.
    """

    def __init__(self, namespace: str) -> None:
        """
        Initialize the UniqueDict with a namespace.

        :param namespace: The namespace for the dictionary.
        """
        super().__init__()
        self.__namespace = namespace

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Set a key-value pair in the dictionary, ensuring the key is unique.

        :param key: The key to set.
        :param value: The value to associate with the key.
        :raises ConfigError: If the key is reused within the namespace.
        """
        if not _is_dunder(key) and key in self:
            raise ConfigError(f"Attempted to reuse {key!r} in {self.__namespace!r}")
        super().__setitem__(key, value)


class MetaBase(type):
    """
    Metaclass for defining configuration and section classes.

    This metaclass provides mechanisms for:
    - Ensuring unique attributes in classes.
    - Enforcing inheritance rules for configurations and sections.
    - Managing class-level members and attribute access.
    """

    @classmethod
    def __prepare__(mcs, name: str, bases: Tuple[Any]) -> UniqueDict:  # type: ignore
        """
        Prepare the class namespace using a UniqueDict.

        :param name: The name of the class.
        :param bases: The base classes of the class.
        :return: A UniqueDict instance to serve as the class namespace.
        """
        return UniqueDict(name)

    def __init__(cls, name: str, bases: Tuple[Any], attrs: Dict[str, Any]) -> None:
        """
        Initialize the metaclass with specified parameters.

        :param name: The name of the class.
        :param bases: The base classes of the class.
        :param attrs: The attributes of the class.
        :raises ConfigError: If inheritance or attribute usage rules are violated.
        """
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
        """
        Retrieve an attribute from the class, resolving FutureValue instances if necessary.

        :param name: The name of the attribute.
        :return: The value of the attribute.
        """
        attr = super().__getattribute__(name)
        if isinstance(attr, FutureValue):
            return attr.get()
        return attr

    def __getattr__(cls, name: str) -> Any:
        """
        Handle attribute access for undefined attributes.

        :param name: The name of the attribute.
        :raises ConfigAttrError: If the attribute does not exist.
        """
        raise ConfigAttrError(f"{name!r} does not exist in <{cls.__get_full_name()}>")

    def __setattr__(cls, name: str, value: Any) -> None:
        """
        Set an attribute on the class, enforcing immutability if the class is frozen.

        :param name: The name of the attribute.
        :param value: The value to set.
        :raises ConfigError: If setting the attribute violates immutability rules.
        """
        if cls.__frozen__ and name != "__frozen__":
            if name in cls:
                raise ConfigError(f"Attempted to override {name!r} in <{cls.__get_full_name()}>")
            raise ConfigError(f"Attempted to add {name!r} to <{cls.__get_full_name()}> at runtime")
        super().__setattr__(name, value)

    def __delattr__(cls, name: str) -> None:
        """
        Prevent attribute deletion.

        :param name: The name of the attribute.
        :raises ConfigError: Always, as attribute deletion is not allowed.
        """
        raise ConfigError(f"Attempted to remove {name!r} from <{cls.__get_full_name()}>")

    def __getitem__(cls, key: str) -> Any:
        """
        Retrieve a class member by key.

        :param key: The key of the member.
        :return: The value of the member.
        :raises ConfigKeyError: If the key does not exist in the class.
        """
        if key in cls:
            return getattr(cls, key)
        raise ConfigKeyError(f"{key!r} does not exist in <{cls.__get_full_name()}>")

    def __setitem__(cls, key: str, value: Any) -> None:
        """
        Set a class member.

        :param key: The key of the member.
        :param value: The value to set.
        """
        return setattr(cls, key, value)

    def __delitem__(cls, key: str) -> None:
        """
        Delete a class member.

        :param key: The key of the member.
        """
        return delattr(cls, key)

    def __call__(cls, *args: Any, **kwargs: Any) -> None:
        """
        Prevent instantiation of the class.

        :raises ConfigError: Always, as instantiation is not allowed.
        """
        if _is_config(cls):
            raise ConfigError(f"Attempted to initialize config <{cls.__get_full_name()}>")
        elif _is_section(cls):
            raise ConfigError(f"Attempted to initialize section <{cls.__get_full_name()}>")
        else:  # pragma: nocover
            pass

    @property
    def __members(cls) -> Dict[str, Any]:
        """
        Retrieve all members of the class, including those inherited.

        :return: A dictionary of class members.
        """
        result = {}

        for base in reversed(cls.__bases__):
            if _is_config(base) or _is_section(base):
                for key in base:  # type: ignore
                    result[key] = ...

        for key in cls.__members__:
            result[key] = ...

        return result

    def __len__(cls) -> int:
        """
        Get the number of members in the class.

        :return: The number of members.
        """
        return len(cls.__members)

    def __iter__(cls) -> Iterator[str]:
        """
        Iterate over the keys of the class members.

        :return: An iterator over the member keys.
        """
        return cls.__members.__iter__()

    def __contains__(cls, item: Any) -> bool:
        """
        Check if a member exists in the class.

        :param item: The key to check.
        :return: True if the member exists, False otherwise.
        """
        return item in cls.__members

    def __repr__(cls) -> str:
        """
        Get a string representation of the class.

        :return: A formatted string representing the class.
        """
        formatted = cls.__format(name=cls.__get_full_name())
        return os.linesep.join(formatted)

    def __get_full_name(cls) -> str:
        """
        Retrieve the fully qualified name of the class.

        :return: The fully qualified name of the class.
        """
        namespace = [cls.__name__]
        parent = cls.__parent__
        while parent is not None:
            namespace += [parent.__name__]
            parent = parent.__parent__
        return ".".join(reversed(namespace))

    def keys(cls) -> KeysView[str]:
        """
        Get the keys of the class members.

        :return: A view of the keys.
        """
        return cls.__members.keys()

    def values(cls) -> ValuesView[Any]:
        """
        Get the values of the class members.

        :return: A view of the values.
        """
        return {key: val for key, val in cls.items()}.values()

    def items(cls) -> ItemsView[str, Any]:
        """
        Get the items of the class members.

        :return: A view of the items.
        """
        items = {}
        for key in cls.__members:
            try:
                items[key] = getattr(cls, key)
            except Exception as e:
                items[key] = e
        return items.items()

    def get(cls, key: str, default: Union[NilType, Any] = Nil) -> Any:
        """
        Retrieve a member by key, or return a default value if the key is not found.

        :param key: The key to retrieve.
        :param default: The default value to return if the key is not found.
        :return: The value of the key, or the default value.
        :raises KeyError: If the key is not found and no default value is provided.
        """
        try:
            return cls[key]
        except KeyError:
            if default is not Nil:
                return default
            raise

    def __prefetch(cls) -> List[str]:
        """
        Prefetch all members of the class, resolving any dependent values.

        :return: A list of error messages, if any.
        """
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
        """
        Prefetch all members and raise an error if any issues occur.

        :raises ConfigEnvError: If there are errors during prefetching.
        """
        errors = cls.__prefetch()
        if len(errors) > 0:
            prefix = os.linesep + "- "
            message = f"Failed to prefetch:{prefix}" + prefix.join(errors)
            raise ConfigEnvError(message)

    def __format(cls, *,
                 indent: int = 0, prepend: bool = False, name: Optional[str] = None) -> List[str]:
        """
        Format the class into a readable string representation.

        :param indent: The level of indentation to apply.
        :param prepend: Whether to prepend an empty line.
        :param name: The name to use for the class (defaults to the class name).
        :return: A list of strings representing the formatted class.
        """
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
        """
        Print the class structure to the specified stream.

        :param stream: The stream to print to (default is sys.stdout).
        """
        warnings.warn("Deprecated: use print(<cls>) instead", DeprecationWarning)
        formatted = os.linesep.join(cls.__format())
        print(formatted, file=stream)


class Section(metaclass=MetaBase):
    """
    Represents a configuration section.

    This class serves as a base for defining sections in a configuration.
    """
    __frozen__: bool = False
    __parent__: Optional[MetaBase] = None
    __members__: Dict[str, Any] = {}


_Section = Section


class Config(metaclass=MetaBase):
    """
    Represents a configuration.

    This class serves as a base for defining configurations.
    """
    __frozen__: bool = False
    __parent__: Optional[MetaBase] = None
    __members__: Dict[str, Any] = {}


_Config = Config
