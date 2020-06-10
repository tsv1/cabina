from typing import Any


class MetaConfig(type):
    def __setattr__(cls, name: Any, value: Any) -> None:
        raise TypeError(f"__setattr__ {name}")

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


class MetaSection(MetaConfig):
    pass


class Section(metaclass=MetaSection):
    pass


class Config(metaclass=MetaConfig):
    pass
