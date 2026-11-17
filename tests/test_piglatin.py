"""Tests for piglatin.translate (this module only)."""

import pytest

from piglatin import translate


def test_worked_examples_verbatim():
    assert translate("apple") == "appleway"
    assert translate("banana") == "ananabay"
    assert translate("string") == "ingstray"


def test_vowel_start_appends_way():
    assert translate("apple") == "appleway"
    assert translate("orange") == "orangeway"
    assert translate("eat") == "eatway"


def test_consonant_start_moves_cluster():
    assert translate("banana") == "ananabay"
    assert translate("string") == "ingstray"
    assert translate("chair") == "airchay"
    assert translate("frog") == "ogfray"


def test_multi_consonant_clusters():
    # "string" -> initial cluster "str"
    assert translate("string") == "ingstray"
    # "chair" -> initial cluster "ch"
    assert translate("chair") == "airchay"
    assert translate("three") == "eethray"


def test_case_preservation_lowercase():
    assert translate("apple") == "appleway"
    assert translate("banana") == "ananabay"
    assert translate("string") == "ingstray"


def test_case_preservation_initial_capital():
    assert translate("Apple") == "Appleway"
    assert translate("Banana") == "Ananabay"
    assert translate("String") == "Ingstray"
    assert translate("Chair") == "Airchay"


def test_empty_string_raises_value_error():
    # Documented choice: empty string is invalid input -> ValueError.
    with pytest.raises(ValueError):
        translate("")


def test_non_string_input_raises_value_error():
    # Documented choice: non-string input -> ValueError.
    with pytest.raises(ValueError):
        translate(123)
    with pytest.raises(ValueError):
        translate(None)


def test_non_alphabetic_input_raises_value_error():
    # Documented choice: input must be a single alphabetic word -> ValueError.
    with pytest.raises(ValueError):
        translate("hi!")
    with pytest.raises(ValueError):
        translate("two words")
