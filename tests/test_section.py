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
