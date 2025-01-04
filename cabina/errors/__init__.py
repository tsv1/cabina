__all__ = (
    "ConfigError", "ConfigAttrError", "ConfigKeyError",
    "EnvError", "EnvKeyError", "EnvParseError", "ConfigEnvError",
    "Error",
)


class Error(Exception):
    """
    Base class for all custom exceptions in the package.

    This class serves as the root of the exception hierarchy for both configuration
    and environment-related errors.
    """
    pass


class ConfigError(TypeError, Error):
    """
    Represents errors related to configuration.

    This exception is raised when there are issues specific to configuration logic
    or improper usage of configuration-related components.
    """
    pass


class ConfigAttrError(AttributeError, ConfigError):
    """
    Represents attribute errors in configuration objects.

    This exception is raised when an invalid or missing attribute is accessed
    in a configuration object.
    """
    pass


class ConfigKeyError(KeyError, ConfigError):
    """
    Represents key errors in configuration objects.

    This exception is raised when an invalid or missing key is accessed
    in a configuration object.
    """

    def __str__(self) -> str:
        """
        Return a string representation of the exception.

        :return: The string representation of the parent `ConfigError` exception.
        """
        return ConfigError.__str__(self)


class EnvError(Error):
    """
    Represents errors related to environment variables.

    This exception is the base class for all exceptions raised when there are
    issues with environment variable retrieval, parsing, or usage.
    """
    pass


class EnvKeyError(KeyError, EnvError):
    """
    Represents key errors in environment variables.

    This exception is raised when an invalid or missing key is accessed
    in the environment.
    """

    def __str__(self) -> str:
        """
        Return a string representation of the exception.

        :return: The string representation of the parent `EnvError` exception.
        """
        return EnvError.__str__(self)


class EnvParseError(TypeError, EnvError):
    """
    Represents parsing errors for environment variables.

    This exception is raised when an environment variable cannot be parsed
    into the expected format or type.
    """
    pass


class ConfigEnvError(ValueError, EnvError, ConfigError):
    """
    Represents errors that involve both configuration and environment variables.

    This exception is raised when there are issues that span both configuration
    and environment-related logic.
    """
    pass
