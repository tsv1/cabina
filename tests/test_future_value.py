from cabina import FutureValue


def test_future_value():
    def accessor():
        return "banana"

    value = FutureValue(accessor)
    assert value.get() == "banana"


def test_future_value_with_args():
    def accessor(*args):
        return args

    value = FutureValue(accessor, 1, 2, 3)
    assert value.get() == (1, 2, 3)


def test_future_value_with_kwargs():
    def accessor(**kwargs):
        return kwargs

    value = FutureValue(accessor, key1="value1", key2="value2")
    assert value.get() == {"key1": "value1", "key2": "value2"}


def test_future_value_get():
    container = [1]

    def accessor():
        return container[0]

    value = FutureValue(accessor)
    assert value.get() == 1

    container[0] = 2
    assert value.get() == 1


def test_future_value_fetch():
    container = [1]

    def accessor():
        return container[0]

    value = FutureValue(accessor)
    assert value.fetch() == 1

    container[0] = 2
    assert value.fetch() == 2


def test_future_value_get_fetch():
    container = [1]

    def accessor():
        return container[0]

    value = FutureValue(accessor)
    assert value.get() == 1

    container[0] = 2
    assert value.fetch() == 2
    assert value.get() == 2


def test_future_value_repr():
    def accessor():
        pass

    # args
    assert repr(FutureValue(accessor, "arg")) == "FutureValue('arg')"
    assert repr(FutureValue(accessor, 1, "arg")) == "FutureValue(1, 'arg')"

    # kwargs
    assert repr(FutureValue(accessor, kwarg="val")) == "FutureValue(kwarg='val')"
    assert (repr(FutureValue(accessor, kwarg1=1, kwarg2="val")) ==
            "FutureValue(kwarg1=1, kwarg2='val')")

    # args & kwargs
    assert (repr(FutureValue(accessor, "arg", default="val")) ==
            "FutureValue('arg', default='val')")
