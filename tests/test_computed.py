from pytest import raises

import cabina
from cabina import computed


def test_computed():
    with raises(Exception) as exc_info:
        class Section(cabina.Section):
            @computed()
            def HOST(cls):
                pass

    assert exc_info.type is TypeError
    assert str(exc_info.value) == "Use @computed instead of @computed()"
