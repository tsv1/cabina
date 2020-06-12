__all__ = ("Error", "ConfigError", "ConfigAttrError", "ConfigKeyError",)


class Error(Exception):
    pass


class ConfigError(TypeError, Error):
    pass


class ConfigAttrError(AttributeError, Error):
    pass


class ConfigKeyError(KeyError, Error):
    def __str__(self) -> str:
        return AttributeError.__str__(self)
