import io
from typing import ItemsView, KeysView, ValuesView

from pytest import raises

import cabina
from cabina.errors import ConfigAttrError, ConfigError, ConfigKeyError


def test_config():
    class Config(cabina.Config):
        pass

    assert issubclass(Config, cabina.Config)
    assert not issubclass(Config, cabina.Section)


def test_config_init_not_allowed():
    class Config(cabina.Config):
        pass

    with raises(Exception) as exc_info:
        Config()

    assert exc_info.type is ConfigError
    assert str(exc_info.value) == "Attempted to initialize config <Config>"


def test_config_options_not_allowed():
    with raises(Exception) as exc_info:
        class Config(cabina.Config):
            DEBUG = False

    assert exc_info.type is ConfigError
    assert str(exc_info.value) == "Attempted to add non-Section 'DEBUG' to <Config>"


def test_config_class_options_not_allowed():
    with raises(Exception) as exc_info:
        class Config(cabina.Config):
            class Main:
                pass

    assert exc_info.type is ConfigError
    assert str(exc_info.value) == "Attempted to add non-Section 'Main' to <Config>"


def test_config_get_attr():
    class Config(cabina.Config):
        class Main(cabina.Section):
            pass

    assert Config.Main == Config.Main


def test_config_get_nonexisting_attr():
    class Config(cabina.Config):
        pass

    with raises(Exception) as exc_info:
        Config.Main

    assert exc_info.type is ConfigAttrError
    assert str(exc_info.value) == "'Main' does not exist in <Config>"


def test_config_set_attr_not_allowed():
    class Config(cabina.Config):
        pass

    class Section(cabina.Section):
        pass

    with raises(Exception) as exc_info:
        Config.Main = Section

    assert exc_info.type is ConfigError
    assert str(exc_info.value) == "Attempted to add 'Main' to <Config> at runtime"


def test_config_override_attr_not_allowed():
    class Config(cabina.Config):
        class Main(cabina.Section):
            pass

    class Section(cabina.Section):
        pass

    with raises(Exception) as exc_info:
        Config.Main = Section

    assert exc_info.type is ConfigError
    assert str(exc_info.value) == "Attempted to override 'Main' in <Config>"


def test_config_del_attr_not_allowed():
    class Config(cabina.Config):
        class Main(cabina.Section):
            pass

    with raises(Exception) as exc_info:
        del Config.Main

    assert exc_info.type is ConfigError
    assert str(exc_info.value) == "Attempted to remove 'Main' from <Config>"


def test_config_get_item():
    class Config(cabina.Config):
        class Main(cabina.Section):
            pass

    assert Config["Main"] == Config.Main


def test_config_get_nonexisting_item():
    class Config(cabina.Config):
        pass

    with raises(Exception) as exc_info:
        Config["Main"]

    assert exc_info.type is ConfigKeyError
    assert str(exc_info.value) == "'Main' does not exist in <Config>"


def test_config_set_item_not_allowed():
    class Config(cabina.Config):
        pass

    class Section(cabina.Section):
        pass

    with raises(Exception) as exc_info:
        Config["Main"] = Section

    assert exc_info.type is ConfigError
    assert str(exc_info.value) == "Attempted to add 'Main' to <Config> at runtime"


def test_config_del_item_not_allowed():
    class Config(cabina.Config):
        class Main(cabina.Section):
            pass

    with raises(Exception) as exc_info:
        del Config["Main"]

    assert exc_info.type is ConfigError
    assert str(exc_info.value) == "Attempted to remove 'Main' from <Config>"


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
    assert Config.get("banana", None) is None

    with raises(Exception) as exc_info:
        Config.get("banana")

    assert exc_info.type is ConfigKeyError
    assert str(exc_info.value) == "'banana' does not exist in <Config>"


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

    assert repr(Conf) == "class <Conf>:\n    ..."


def test_config_unique_keys():
    with raises(Exception) as exc_info:
        class Config(cabina.Config):
            class Main(cabina.Section):
                pass

            class Main(cabina.Section):  # noqa: F811
                pass

    assert exc_info.type is ConfigError
    assert str(exc_info.value) == "Attempted to reuse 'Main' in 'Config'"


def test_config_reserved_keys():
    reserved_keys = [key for key in dir(cabina.Config.__class__) if not key.startswith("__")]

    for reserved_key in reserved_keys:
        with raises(Exception) as exc_info:
            type("Config", (cabina.Config,), {reserved_key: cabina.Section})

        assert exc_info.type is ConfigError
        assert str(exc_info.value) == f"Attempted to use reserved {reserved_key!r} in 'Config'"


def test_config_print():
    class Config(cabina.Config):
        pass

    stream = io.StringIO()
    Config.print(stream)

    assert stream.getvalue() == "\n".join([
        "class <Config>:",
        "    ...",
        "",
    ])


def test_config_with_sections_print():
    class Config(cabina.Config):
        class First(cabina.Section):
            pass

        class Second(cabina.Section):
            pass

    stream = io.StringIO()
    Config.print(stream)

    assert stream.getvalue() == "\n".join([
        "class <Config>:",
        "",
        "    class <First>:",
        "        ...",
        "",
        "    class <Second>:",
        "        ...",
        ""
    ])


def test_config_with_section_print():
    class Config(cabina.Config):
        class Main(cabina.Section):
            DEBUG = False

    stream = io.StringIO()
    Config.print(stream)

    assert stream.getvalue() == "\n".join([
        "class <Config>:",
        "",
        "    class <Main>:",
        "        DEBUG = False",
        ""
    ])
