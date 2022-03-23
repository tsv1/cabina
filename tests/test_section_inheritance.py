from typing import ItemsView

from pytest import raises

import cabina
from cabina.errors import ConfigAttrError, ConfigError


def test_section_inheritance():
    class Section(cabina.Section):
        DEBUG = False

    class AnotherSection(Section):
        pass

    assert Section.DEBUG == AnotherSection.DEBUG


def test_section_inheritance_overriding():
    class Section(cabina.Section):
        DEBUG = False

    class AnotherSection(Section):
        DEBUG = True
        TZ = "UTC"

    assert Section.DEBUG != AnotherSection.DEBUG
    assert AnotherSection.TZ == "UTC"

    with raises(Exception) as exc_info:
        Section.TZ

    assert exc_info.type is ConfigAttrError
    assert str(exc_info.value) == "'TZ' does not exist in <Section>"


def test_section_multiple_inheritance():
    class Section(cabina.Section):
        HOST = "localhost"
        PORT = 5000

    class AnotherSection(cabina.Section):
        PORT = 8080
        DEBUG = False

    class InheritedSection(AnotherSection, Section):
        pass

    assert InheritedSection.DEBUG is False
    assert InheritedSection.HOST == "localhost"
    assert InheritedSection.PORT == 8080


def test_section_invalid_multiple_inheritance():
    with raises(Exception) as exc_info:
        class Section(cabina.Section, dict):
            pass

    assert exc_info.type is ConfigError
    assert str(exc_info.value) == f"Attempted to inherit {dict}"


def test_inherited_section_len():
    class Section(cabina.Section):
        API_HOST = "localhost"
        API_PORT = 8080

    class AnotherSection(Section):
        DEBUG = False

    assert len(AnotherSection) == 3


def test_inherited_section_iter():
    class Section(cabina.Section):
        API_HOST = "localhost"
        API_PORT = 8080

    class AnotherSection(Section):
        DEBUG = False

    options = [option for option in AnotherSection]
    assert options == ["API_HOST", "API_PORT", "DEBUG"]


def test_inherited_section_contains():
    class Section(cabina.Section):
        API_HOST = "localhost"
        API_PORT = 8080

    class AnotherSection(Section):
        DEBUG = False

    assert "DEBUG" in AnotherSection
    assert "API_HOST" in AnotherSection
    assert "API_PORT" in AnotherSection
    assert "banana" not in AnotherSection


def test_inherited_section_items():
    class Section(cabina.Section):
        API_HOST = "localhost"
        API_PORT = 8080

    class AnotherSection(Section):
        DEBUG = False

    assert isinstance(AnotherSection.items(), ItemsView)
    assert list(AnotherSection.items()) == [
        ("API_HOST", "localhost"),
        ("API_PORT", 8080),
        ("DEBUG", False),
    ]
