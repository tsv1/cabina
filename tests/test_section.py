from pytest import raises

import cabina


def test_section():
    class Main(cabina.Section):
        pass

    assert issubclass(Main, cabina.Section)
    assert not issubclass(Main, cabina.Config)


def test_section_init():
    class Main(cabina.Section):
        pass

    with raises(TypeError):
        Main()


def test_config_attr_get():
    class Main(cabina.Section):
        API_HOST = "localhost"
        API_PORT = 8080

    assert Main.API_HOST == "localhost"
    assert Main.API_PORT == 8080


def test_config_attr_set():
    class Main(cabina.Section):
        API_HOST = "localhost"

    with raises(TypeError):
        Main.API_HOST = "127.0.0.1"


def test_config_attr_del():
    class Main(cabina.Section):
        API_HOST = "localhost"

    with raises(TypeError):
        del Main.API_HOST


def test_config_item_get():
    class Main(cabina.Section):
        API_HOST = "localhost"
        API_PORT = 8080

    assert Main["API_HOST"] == "localhost"
    assert Main["API_PORT"] == 8080


def test_config_item_set():
    class Main(cabina.Section):
        API_HOST = "localhost"

    with raises(TypeError):
        Main["API_HOST"] = "127.0.0.1"


def test_config_item_del():
    class Main(cabina.Section):
        API_HOST = "localhost"

    with raises(TypeError):
        del Main["API_HOST"]
