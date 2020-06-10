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


def test_section_attr_get():
    class Main(cabina.Section):
        API_HOST = "localhost"
        API_PORT = 8080

    assert Main.API_HOST == "localhost"
    assert Main.API_PORT == 8080


def test_section_attr_set():
    class Main(cabina.Section):
        API_HOST = "localhost"

    with raises(TypeError):
        Main.API_HOST = "127.0.0.1"


def test_section_attr_del():
    class Main(cabina.Section):
        API_HOST = "localhost"

    with raises(TypeError):
        del Main.API_HOST


def test_section_item_get():
    class Main(cabina.Section):
        API_HOST = "localhost"
        API_PORT = 8080

    assert Main["API_HOST"] == "localhost"
    assert Main["API_PORT"] == 8080


def test_section_item_set():
    class Main(cabina.Section):
        API_HOST = "localhost"

    with raises(TypeError):
        Main["API_HOST"] = "127.0.0.1"


def test_section_item_del():
    class Main(cabina.Section):
        API_HOST = "localhost"

    with raises(TypeError):
        del Main["API_HOST"]


def test_section_len_no_sections():
    class Main(cabina.Section):
        pass

    assert len(Main) == 0


def test_section_len_with_sections():
    class Main(cabina.Section):
        API_HOST = "localhost"
        API_PORT = 8080

    assert len(Main) == 2
