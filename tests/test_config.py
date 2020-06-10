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


def test_config_option():
    with raises(TypeError):
        class Config(cabina.Config):
            DEBUG = False


def test_config_cls_option():
    with raises(TypeError):
        class Config(cabina.Config):
            class Main:
                pass


def test_config_attr_get():
    class Config(cabina.Config):
        class Main(cabina.Section):
            pass

    assert Config.Main == Config.Main


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


def test_config_len_no_sections():
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
