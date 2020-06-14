__all__ = ("ConfigError", "ConfigAttrError", "ConfigKeyError",
           "EnvError", "EnvKeyError", "EnvParseError", "Error",)


class Error(Exception):
    pass


class ConfigError(TypeError, Error):
    pass


class ConfigAttrError(AttributeError, ConfigError):
    pass


class ConfigKeyError(KeyError, ConfigError):
    def __str__(self) -> str:
        return AttributeError.__str__(self)


class EnvError(Error):
    pass


class EnvKeyError(KeyError, EnvError):
    pass


class EnvParseError(TypeError, EnvError):
    pass
