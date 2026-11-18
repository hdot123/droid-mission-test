"""Tests for slugify.slugify (ASCII URL slug rules)."""

from slugify import slugify


def test_hello_world():
    assert slugify("Hello, World!") == "hello-world"


def test_spaces_collapse_and_trim():
    assert slugify("  A  B  ") == "a-b"


def test_only_punctuation_is_empty():
    assert slugify("!!!") == ""


def test_non_ascii_letter_treated_as_separator():
    assert slugify("café") == "caf"


def test_already_slug_unchanged():
    assert slugify("already-slug") == "already-slug"


def test_empty_string():
    assert slugify("") == ""
