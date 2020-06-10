from pytest import raises

import cabina


def test_config():
    class Config(cabina.Config):
        pass

    assert issubclass(Config, cabina.Config)
    assert not issubclass(Config, cabina.Section)


def test_config_init():
    class Config(cabina.Config):
        pass

    with raises(TypeError):
        Config()


def test_config_attr_get():
    class Config(cabina.Config):
        class Main(cabina.Section):
            pass

    assert Config.Main


def test_config_attr_set():
    class Config(cabina.Config):
        pass

    class Section(cabina.Section):
        pass

    with raises(TypeError):
        Config.Main = Section


def test_config_attr_del():
    class Config(cabina.Config):
        class Main(cabina.Section):
            pass

    with raises(TypeError):
        del Config.Main


def test_config_item_get():
    class Config(cabina.Config):
        class Main(cabina.Section):
            pass

    assert Config["Main"] == Config.Main


def test_config_item_set():
    class Config(cabina.Config):
        pass

    class Section(cabina.Section):
        pass

    with raises(TypeError):
        Config["Main"] = Section


def test_config_item_del():
    class Config(cabina.Config):
        class Main(cabina.Section):
            pass

    with raises(TypeError):
        del Config["Main"]
