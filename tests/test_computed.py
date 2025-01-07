from pytest import raises

import cabina
from cabina import computed
from cabina.errors import ConfigError


def test_computed():
    with raises(Exception) as exc_info:
        class Section(cabina.Section):
            @computed()
            def HOST(cls):
                pass

    assert exc_info.type is TypeError
    assert str(exc_info.value) == "Use @computed instead of @computed()"


def test_computed_accessing_unknown_attribute():
    class App(cabina.Section):
        @computed
        def HOST(cls):
            return cls.unknown

    with raises(Exception) as exc_info:
        App.HOST

    assert exc_info.type is ConfigError
    assert str(exc_info.value) == (
        "Failed to return @computed 'HOST' ('unknown' does not exist in <App>)"
    )


def test_computed_accessing_invalid_object_attribute():
    class App(cabina.Section):
        @computed
        def HOST(cls):
            return object.uknown

    with raises(Exception) as exc_info:
        App.HOST

    assert exc_info.type is ConfigError
    assert str(exc_info.value) == (
        "Failed to return @computed 'HOST' (type object 'object' has no attribute 'uknown')"
    )
