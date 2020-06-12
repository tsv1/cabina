from typing import ItemsView, KeysView, ValuesView

from pytest import raises

import cabina
from cabina.errors import ConfigError


def test_config():
    class Config(cabina.Config):
        pass

    assert issubclass(Config, cabina.Config)
    assert not issubclass(Config, cabina.Section)


def test_config_init_not_allowed():
    class Config(cabina.Config):
        pass

    with raises(Exception) as exception:
        Config()

    assert exception.type is ConfigError
    assert str(exception.value) == f"Attempted to initialize {Config!r}"


def test_config_options_not_allowed():
    with raises(Exception) as exception:
        class Config(cabina.Config):
            DEBUG = False

    assert exception.type is ConfigError
    assert str(exception.value) == "Attempted to add non-Section 'DEBUG' to <Config>"


def test_config_class_options_not_allowed():
    with raises(Exception) as exception:
        class Config(cabina.Config):
            class Main:
                pass

    assert exception.type is ConfigError
    assert str(exception.value) == "Attempted to add non-Section 'Main' to <Config>"


def test_config_get_attr():
    class Config(cabina.Config):
        class Main(cabina.Section):
            pass

    assert Config.Main == Config.Main


def test_config_get_nonexisting_attr():
    pass


def test_config_set_attr_not_allowed():
    class Config(cabina.Config):
        pass

    class Section(cabina.Section):
        pass

    with raises(Exception) as exception:
        Config.Main = Section

    assert exception.type is ConfigError
    assert str(exception.value) == f"Attempted to add 'Main' to {Config!r} at runtime"


def test_config_del_attr_not_allowed():
    class Config(cabina.Config):
        class Main(cabina.Section):
            pass

    with raises(Exception) as exception:
        del Config.Main

    assert exception.type is ConfigError
    assert str(exception.value) == f"Attempted to remove 'Main' from {Config!r}"


def test_config_get_item():
    class Config(cabina.Config):
        class Main(cabina.Section):
            pass

    assert Config["Main"] == Config.Main


def test_config_get_nonexisting_item():
    pass


def test_config_set_item_not_allowed():
    class Config(cabina.Config):
        pass

    class Section(cabina.Section):
        pass

    with raises(Exception) as exception:
        Config["Main"] = Section


def test_config_del_item_not_allowed():
    class Config(cabina.Config):
        class Main(cabina.Section):
            pass

    with raises(Exception) as exception:
        del Config["Main"]


def test_config_len_without_sections():
    class Config(cabina.Config):
        pass

    assert len(Config) == 0


def test_config_len_with_sections():
    class Config(cabina.Config):
        class First(cabina.Section):
            pass

        class Second(cabina.Section):
            pass

    assert len(Config) == 2


def test_config_iter_without_sections():
    class Config(cabina.Config):
        pass

    sections = [section for section in Config]
    assert sections == []


def test_config_iter_with_sections():
    class Config(cabina.Config):
        class First(cabina.Section):
            pass

        class Second(cabina.Section):
            pass

    sections = [section for section in Config]
    assert sections == ["First", "Second"]


def test_config_contains():
    class Config(cabina.Config):
        class Main(cabina.Section):
            pass

    assert "Main" in Config
    assert "banana" not in Config


def test_config_keys():
    class Config(cabina.Config):
        class First(cabina.Section):
            pass

        class Second(cabina.Section):
            pass

    assert isinstance(Config.keys(), KeysView)
    assert list(Config.keys()) == ["First", "Second"]


def test_config_values():
    class Config(cabina.Config):
        class First(cabina.Section):
            pass

        class Second(cabina.Section):
            pass

    assert isinstance(Config.values(), ValuesView)
    assert list(Config.values()) == [Config.First, Config.Second]


def test_config_items():
    class Config(cabina.Config):
        class First(cabina.Section):
            pass

        class Second(cabina.Section):
            pass

    assert isinstance(Config.items(), ItemsView)
    assert list(Config.items()) == [
        ("First", Config.First),
        ("Second", Config.Second)
    ]


def test_config_get():
    class Config(cabina.Config):
        class Main(cabina.Section):
            pass

    assert Config.get("Main") == Config.Main

    with raises(Exception) as exception:
        Config.get("banana")

    assert Config.get("banana", None) is None


def test_config_eq():
    class Config1(cabina.Config):
        pass

    class Config2(cabina.Config):
        pass

    assert Config1 == Config1
    assert Config1 != Config2


def test_config_repr():
    class Conf(cabina.Config):
        pass

    assert repr(Conf) == "<Conf>"


def test_config_unique_keys():
    with raises(Exception) as exception:
        class Config(cabina.Config):
            class Main(cabina.Section):
                pass

            class Main(cabina.Section):  # noqa: F811
                pass

    assert exception.type is ConfigError
    assert str(exception.value) == "Attempted to reuse 'Main' in 'Config'"
