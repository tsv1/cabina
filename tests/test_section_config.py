import cabina


def test_section_cabinaig():
    class Config(cabina.Config, cabina.Section):
        pass

    assert issubclass(Config, cabina.Config)
    assert issubclass(Config, cabina.Section)
