__all__ = ("ConfigError", "ConfigAttrError", "ConfigKeyError",
           "EnvError", "EnvKeyError", "EnvParseError", "ConfigEnvError",
           "Error",)


class Error(Exception):
    pass


class ConfigError(TypeError, Error):
    pass


class ConfigAttrError(AttributeError, ConfigError):
    pass


class ConfigKeyError(KeyError, ConfigError):
    def __str__(self) -> str:
        return ConfigError.__str__(self)


class EnvError(Error):
    pass


class EnvKeyError(KeyError, EnvError):
    def __str__(self) -> str:
        return EnvError.__str__(self)


class EnvParseError(TypeError, EnvError):
    pass


class ConfigEnvError(ValueError, EnvError, ConfigError):
    pass
