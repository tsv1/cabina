from typing import ItemsView, KeysView, ValuesView

from pytest import raises

import cabina


def test_section_config():
    class Config(cabina.Config, cabina.Section):
        pass

    assert issubclass(Config, cabina.Config)
    assert issubclass(Config, cabina.Section)


def test_section_config_get_attr():
    class Config(cabina.Config, cabina.Section):
        HOST = "localhost"

        class Main(cabina.Section):
            pass

    assert Config.Main == Config.Main
    assert Config.HOST == "localhost"


def test_section_config_set_attr_not_allowed():
    class Config(cabina.Config, cabina.Section):
        HOST = "localhost"

        class Main(cabina.Section):
            pass

    class Section(cabina.Section):
        pass

    with raises(TypeError):
        Config.HOST = "127.0.0.1"

    with raises(TypeError):
        Config.Main = Section


def test_section_config_del_attr_not_allowed():
    class Config(cabina.Config, cabina.Section):
        HOST = "localhost"

        class Main(cabina.Section):
            pass

    with raises(TypeError):
        del Config.Main

    with raises(TypeError):
        del Config.HOST


def test_section_config_get_item():
    class Config(cabina.Config, cabina.Section):
        HOST = "localhost"

        class Main(cabina.Section):
            pass

    assert Config["Main"] == Config.Main
    assert Config["HOST"] == "localhost"


def test_section_config_set_item_not_allowed():
    class Config(cabina.Config, cabina.Section):
        HOST = "localhost"

        class Main(cabina.Section):
            pass

    class Section(cabina.Section):
        pass

    with raises(TypeError):
        Config["HOST"] = "127.0.0.1"

    with raises(TypeError):
        Config["Main"] = Section


def test_section_config_del_item_not_allowed():
    class Config(cabina.Config, cabina.Section):
        HOST = "localhost"

        class Main(cabina.Section):
            pass

    with raises(TypeError):
        del Config["Main"]

    with raises(TypeError):
        del Config["HOST"]


def test_section_config_len_without_members():
    class Config(cabina.Config, cabina.Section):
        pass

    assert len(Config) == 0


def test_section_config_len_with_sections():
    class Config(cabina.Config, cabina.Section):
        class First(cabina.Section):
            pass

        class Second(cabina.Section):
            pass

    assert len(Config) == 2


def test_section_config_len_with_options():
    class Config(cabina.Config, cabina.Section):
        API_HOST = "localhost"
        API_PORT = 8080

    assert len(Config) == 2


def test_section_config_len_with_members():
    class Config(cabina.Config, cabina.Section):
        API_HOST = "localhost"
        API_PORT = 8080

        class Main(cabina.Section):
            DEBUG = False

    assert len(Config) == 3


def test_section_config_iter_without_members():
    class Config(cabina.Config, cabina.Section):
        pass

    members = [member for member in Config]
    assert members == []


def test_section_config_iter_with_members():
    class Config(cabina.Config, cabina.Section):
        API_HOST = "localhost"
        API_PORT = 8080

        class Main(cabina.Section):
            DEBUG = False

    members = [member for member in Config]
    assert members == ["API_HOST", "API_PORT", "Main"]


def test_section_config_contains():
    class Config(cabina.Config, cabina.Section):
        API_HOST = "localhost"
        API_PORT = 8080

        class Main(cabina.Section):
            DEBUG = False

    assert "API_HOST" in Config
    assert "Main" in Config
    assert "DEBUG" not in Config
    assert "DEBUG" in Config.Main


def test_section_config_keys():
    class Config(cabina.Config, cabina.Section):
        API_HOST = "localhost"
        API_PORT = 8080

        class Main(cabina.Section):
            DEBUG = False

    assert isinstance(Config.keys(), KeysView)
    assert list(Config.keys()) == ["API_HOST", "API_PORT", "Main"]


def test_section_config_values():
    class Config(cabina.Config, cabina.Section):
        API_HOST = "localhost"
        API_PORT = 8080

        class Main(cabina.Section):
            DEBUG = False

    assert isinstance(Config.values(), ValuesView)
    assert list(Config.values()) == ["localhost", 8080, Config.Main]


def test_section_config_items():
    class Config(cabina.Config, cabina.Section):
        API_HOST = "localhost"
        API_PORT = 8080

        class Main(cabina.Section):
            DEBUG = False

    assert isinstance(Config.items(), ItemsView)
    assert list(Config.items()) == [
        ("API_HOST", "localhost"),
        ("API_PORT", 8080),
        ("Main", Config.Main)
    ]


def test_section_config_get():
    class Config(cabina.Config, cabina.Section):
        API_HOST = "localhost"

        class Main(cabina.Section):
            pass

    assert Config.get("Main") == Config.Main
    assert Config.get("API_HOST") == Config.API_HOST

    with raises(KeyError):
        Config.get("banana")

    assert Config.get("banana", None) is None


def test_section_config_eq():
    class Config1(cabina.Config, cabina.Section):
        pass

    class Config2(cabina.Config, cabina.Section):
        pass

    assert Config1 == Config1
    assert Config1 != Config2


def test_section_config_repr():
    class Conf(cabina.Config, cabina.Section):
        pass

    assert repr(Conf) == "<Conf>"


def test_section_config_unique_keys():
    with raises(TypeError):
        class Config1(cabina.Config, cabina.Section):
            class Main(cabina.Section):
                pass

            class Main(cabina.Section):  # noqa: F811
                pass

    with raises(TypeError):
        class Config2(cabina.Config, cabina.Section):
            DEBUG = True
            DEBUG = False
