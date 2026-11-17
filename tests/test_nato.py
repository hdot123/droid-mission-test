"""Tests for nato.py only."""

import pytest

import nato


def test_worked_example_cat():
    assert nato.spell("cat") == "Charlie-Alfa-Tango"


def test_worked_example_go():
    assert nato.spell("Go") == "Golf-Oscar"


def test_case_insensitive():
    assert nato.spell("CAT") == nato.spell("cat")
    assert nato.spell("cAt") == "Charlie-Alfa-Tango"


def test_hyphen_joining():
    assert nato.spell("abc") == "Alfa-Bravo-Charlie"
    result = nato.spell("hello")
    assert result.count("-") == 4
    assert result.split("-") == [
        "Hotel",
        "Echo",
        "Lima",
        "Lima",
        "Oscar",
    ]


@pytest.mark.parametrize("bad", ["c4t", "hi you", "a-b", "", "a!", "cat."])
def test_value_error_on_non_letter(bad):
    with pytest.raises(ValueError):
        nato.spell(bad)
