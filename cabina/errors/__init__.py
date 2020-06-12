__all__ = ("Error", "ConfigError", "ConfigAttrError", "ConfigKeyError",)


class Error(Exception):
    pass


class ConfigError(TypeError, Error):
    pass


class ConfigAttrError(AttributeError, Error):
    pass


class ConfigKeyError(KeyError, Error):
    pass
