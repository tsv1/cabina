from cabina import Environment


def test_env():
    env = Environment({"<key>": "banana"})
    assert env("<key>") == "banana"


def test_env_none():
    env = Environment({"<key>": "None"})
    assert env.none("<key>") is None


def test_env_bool():
    env = Environment({"<key>": "True"})
    assert env.bool("<key>") is True


def test_env_int():
    env = Environment({"<key>": "42"})
    assert env.int("<key>") == 42


def test_env_float():
    env = Environment({"<key>": "3.14"})
    assert env.float("<key>") == 3.14


def test_env_str():
    env = Environment({"<key>": "banana "})
    assert env.str("<key>") == "banana"


def test_env_tuple():
    env = Environment({"<key>": "first, second"})
    assert env.tuple("<key>") == ("first", "second",)


def test_env_tuple_with_separator():
    env = Environment({"<key>": "first second"})
    assert env.tuple("<key>", separator=" ") == ("first", "second",)
