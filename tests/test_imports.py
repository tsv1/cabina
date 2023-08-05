# flake8: noqa
from pytest import raises


def test_import_config():
    from cabina import Config


def test_import_section():
    from cabina import Section


def test_import_computed():
    from cabina import computed


def test_import_meta():
    from cabina import MetaBase


def test_import_error():
    from cabina.errors import Error
    with raises(ImportError):
        from cabina import Error


def test_import_config_error():
    from cabina.errors import ConfigError
    with raises(ImportError):
        from cabina import ConfigError


def test_import_config_attr_error():
    from cabina.errors import ConfigAttrError
    with raises(ImportError):
        from cabina import ConfigAttrError


def test_import_config_key_error():
    from cabina.errors import ConfigKeyError
    with raises(ImportError):
        from cabina import ConfigKeyError


def test_import_env_error():
    from cabina.errors import EnvError
    with raises(ImportError):
        from cabina import EnvError


def test_import_env_key_error():
    from cabina.errors import EnvKeyError
    with raises(ImportError):
        from cabina import EnvKeyError


def test_import_env_parse_error():
    from cabina.errors import EnvParseError
    with raises(ImportError):
        from cabina import EnvParseError


def test_import_config_env_error():
    from cabina.errors import ConfigEnvError
    with raises(ImportError):
        from cabina import ConfigEnvError


def test_import_environment():
    from cabina import Environment


def test_import_env():
    from cabina import env


def test_import_lazy_environment():
    from cabina import LazyEnvironment


def test_import_lazy_env():
    from cabina import lazy_env


def test_import_future_value():
    from cabina import FutureValue


def test_import_value_type():
    from cabina import ValueType


def test_import_parser_parse_as_is():
    from cabina.parsers import parse_as_is
    with raises(ImportError):
        from cabina import parse_as_is


def test_import_parser_parse_none():
    from cabina.parsers import parse_none
    with raises(ImportError):
        from cabina import parse_none


def test_import_parser_parse_bool():
    from cabina.parsers import parse_bool
    with raises(ImportError):
        from cabina import parse_bool


def test_import_parser_parse_int():
    from cabina.parsers import parse_int
    with raises(ImportError):
        from cabina import parse_int


def test_import_parser_parse_float():
    from cabina.parsers import parse_float
    with raises(ImportError):
        from cabina import parse_float


def test_import_parser_parse_str():
    from cabina.parsers import parse_str
    with raises(ImportError):
        from cabina import parse_str


def test_import_parser_parse_tuple():
    from cabina.parsers import parse_tuple
    with raises(ImportError):
        from cabina import parse_tuple
