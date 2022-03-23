from typing import ItemsView, KeysView, ValuesView

from pytest import raises

import cabina
from cabina.errors import ConfigAttrError, ConfigError


def test_config_inheritance():
    class Config(cabina.Config):
        class Main(cabina.Section):
            DEBUG = False

    class AnotherConfig(Config):
        pass

    assert Config.Main == AnotherConfig.Main
    assert Config.Main.DEBUG == AnotherConfig.Main.DEBUG


def test_config_inheritance_overriding():
    class Config(cabina.Config):
        class Main(cabina.Section):
            DEBUG = False

    class AnotherConfig(Config):
        class Main(cabina.Section):
            DEBUG = True
            TZ = "UTC"

    assert Config.Main != AnotherConfig.Main
    assert Config.Main.DEBUG != AnotherConfig.Main.DEBUG
    assert AnotherConfig.Main.TZ == "UTC"

    with raises(Exception) as exc_info:
        Config.Main.TZ

    assert exc_info.type is ConfigAttrError
    assert str(exc_info.value) == "'TZ' does not exist in <Config.Main>"


def test_config_multiple_inheritance():
    class Config(cabina.Config):
        class Main(cabina.Section):
            DEBUG = True
            HOST = "localhost"

    class AnotherConfig(cabina.Config):
        class Main(cabina.Section):
            DEBUG = False
            PORT = 5000

    class InheritedConfig(Config, AnotherConfig):
        pass

    assert InheritedConfig.Main.DEBUG is True
    assert InheritedConfig.Main.HOST == "localhost"

    with raises(Exception) as exc_info:
        InheritedConfig.Main.PORT

    assert exc_info.type is ConfigAttrError


def test_config_invalid_multiple_inheritance():
    with raises(Exception) as exc_info:
        class Config(cabina.Config, dict):
            pass

    assert exc_info.type is ConfigError
    assert str(exc_info.value) == f"Attempted to inherit {dict}"


def test_inherited_config_len():
    class Config(cabina.Config):
        class First(cabina.Section):
            pass

    class AnotherConfig(Config):
        class Second(cabina.Section):
            pass

    assert len(AnotherConfig) == 2


def test_inherited_config_iter():
    class Config(cabina.Config):
        class First(cabina.Section):
            pass

    class AnotherConfig(Config):
        class Second(cabina.Section):
            pass

    sections = [section for section in AnotherConfig]
    assert sections == ["First", "Second"]


def test_inherited_config_contains():
    class Config(cabina.Config):
        class First(cabina.Section):
            pass

    class AnotherConfig(Config):
        class Second(cabina.Section):
            pass

    assert "First" in AnotherConfig
    assert "Second" in AnotherConfig
    assert "Third" not in AnotherConfig


def test_inherited_config_items():
    class Config(cabina.Config):
        class First(cabina.Section):
            pass

    class AnotherConfig(Config):
        class Second(cabina.Section):
            pass

    assert isinstance(AnotherConfig.keys(), KeysView)
    assert list(AnotherConfig.keys()) == ["First", "Second"]

    assert isinstance(AnotherConfig.values(), ValuesView)
    assert list(AnotherConfig.values()) == [AnotherConfig.First, AnotherConfig.Second]

    assert isinstance(AnotherConfig.items(), ItemsView)
    assert list(AnotherConfig.items()) == [
        ("First", AnotherConfig.First),
        ("Second", AnotherConfig.Second)
    ]
