from typing import ItemsView, KeysView, ValuesView

from pytest import raises

import cabina


def test_section():
    class Main(cabina.Section):
        pass

    assert issubclass(Main, cabina.Section)
    assert not issubclass(Main, cabina.Config)


def test_section_init_not_allowed():
    class Main(cabina.Section):
        pass

    with raises(TypeError):
        Main()


def test_section_get_attr():
    class Main(cabina.Section):
        API_HOST = "localhost"
        API_PORT = 8080

    assert Main.API_HOST == "localhost"
    assert Main.API_PORT == 8080


def test_section_set_attr_not_allowed():
    class Main(cabina.Section):
        API_HOST = "localhost"

    with raises(TypeError):
        Main.API_HOST = "127.0.0.1"


def test_section_del_attr_not_allowed():
    class Main(cabina.Section):
        API_HOST = "localhost"

    with raises(TypeError):
        del Main.API_HOST


def test_section_get_item():
    class Main(cabina.Section):
        API_HOST = "localhost"
        API_PORT = 8080

    assert Main["API_HOST"] == "localhost"
    assert Main["API_PORT"] == 8080


def test_section_set_item_not_allowed():
    class Main(cabina.Section):
        API_HOST = "localhost"

    with raises(TypeError):
        Main["API_HOST"] = "127.0.0.1"


def test_section_del_item_not_allowed():
    class Main(cabina.Section):
        API_HOST = "localhost"

    with raises(TypeError):
        del Main["API_HOST"]


def test_section_len_without_options():
    class Main(cabina.Section):
        pass

    assert len(Main) == 0


def test_section_len_with_options():
    class Main(cabina.Section):
        API_HOST = "localhost"
        API_PORT = 8080

    assert len(Main) == 2


def test_section_iter_without_options():
    class Main(cabina.Section):
        pass

    options = [option for option in Main]
    assert options == []


def test_section_iter_with_options():
    class Main(cabina.Section):
        API_HOST = "localhost"
        API_PORT = 8080

    options = [option for option in Main]
    assert options == ["API_HOST", "API_PORT"]


def test_section_contains():
    class Main(cabina.Section):
        DEBUG = False

    assert "DEBUG" in Main
    assert "banana" not in Main


def test_section_keys():
    class Main(cabina.Section):
        API_HOST = "localhost"
        API_PORT = 8080

    assert isinstance(Main.keys(), KeysView)
    assert list(Main.keys()) == ["API_HOST", "API_PORT"]


def test_section_kwargs():
    class Main(cabina.Section):
        host = "localhost"
        port = 8080
        debug = False

    def connect(host, port, **kwargs):
        return host, port

    assert connect(**Main) == (Main.host, Main.port)


def test_section_values():
    class Main(cabina.Section):
        API_HOST = "localhost"
        API_PORT = 8080

    assert isinstance(Main.values(), ValuesView)
    assert list(Main.values()) == ["localhost", 8080]


def test_section_items():
    class Main(cabina.Section):
        API_HOST = "localhost"
        API_PORT = 8080

    assert isinstance(Main.items(), ItemsView)
    assert list(Main.items()) == [
        ("API_HOST", "localhost"),
        ("API_PORT", 8080)
    ]


def test_config_get():
    class Main(cabina.Section):
        API_HOST = "localhost"

    assert Main.get("API_HOST") == Main.API_HOST

    with raises(KeyError):
        Main.get("banana")

    assert Main.get("banana", None) is None


def test_section_eq():
    class Section1(cabina.Section):
        pass

    class Section2(cabina.Section):
        pass

    assert Section1 == Section1
    assert Section1 != Section2
