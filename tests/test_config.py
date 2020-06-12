from typing import ItemsView, KeysView, ValuesView

from pytest import raises

import cabina


def test_config():
    class Config(cabina.Config):
        pass

    assert issubclass(Config, cabina.Config)
    assert not issubclass(Config, cabina.Section)


def test_config_init_not_allowed():
    class Config(cabina.Config):
        pass

    with raises(TypeError):
        Config()


def test_config_options_not_allowed():
    with raises(TypeError):
        class Config(cabina.Config):
            DEBUG = False


def test_config_class_options_not_allowed():
    with raises(TypeError):
        class Config(cabina.Config):
            class Main:
                pass


def test_config_get_attr():
    class Config(cabina.Config):
        class Main(cabina.Section):
            pass

    assert Config.Main == Config.Main


def test_config_set_attr_not_allowed():
    class Config(cabina.Config):
        pass

    class Section(cabina.Section):
        pass

    with raises(TypeError):
        Config.Main = Section


def test_config_del_attr_not_allowed():
    class Config(cabina.Config):
        class Main(cabina.Section):
            pass

    with raises(TypeError):
        del Config.Main


def test_config_get_item():
    class Config(cabina.Config):
        class Main(cabina.Section):
            pass

    assert Config["Main"] == Config.Main


def test_config_set_item_not_allowed():
    class Config(cabina.Config):
        pass

    class Section(cabina.Section):
        pass

    with raises(TypeError):
        Config["Main"] = Section


def test_config_del_item_not_allowed():
    class Config(cabina.Config):
        class Main(cabina.Section):
            pass

    with raises(TypeError):
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

    with raises(KeyError):
        Config.get("banana")

    assert Config.get("banana", None) is None


def test_config_eq():
    class Config1(cabina.Config):
        pass

    class Config2(cabina.Config):
        pass

    assert Config1 == Config1
    assert Config1 != Config2
