import cabina


def test_section_config():
    class Config(cabina.Config, cabina.Section):
        pass

    assert issubclass(Config, cabina.Config)
    assert issubclass(Config, cabina.Section)


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
