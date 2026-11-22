"""Tests for slugify.slugify."""

from slugify import slugify


def test_hello_world():
    assert slugify("Hello World!") == "hello-world"


def test_underscores_and_repeated_spaces():
    assert slugify("a__b  c") == "a-b-c"


def test_leading_trailing_hyphens():
    assert slugify("--Hi--") == "hi"


def test_empty_string():
    assert slugify("") == ""


def test_only_punctuation():
    assert slugify("!!!...???") == ""
    assert slugify("!!!") == ""


def test_unicode_and_punctuation_heavy():
    assert slugify("Café — Déjà Vu!") == "caf-dj-vu"
    assert slugify("a @ b # c $ d") == "a-b-c-d"


def test_digits():
    assert slugify("Version 2.0 Release!") == "version-20-release"
    assert slugify("42") == "42"


def test_repeated_spaces_collapse():
    assert slugify("hello     world") == "hello-world"


def test_mixed_case_and_underscores():
    assert slugify("Hello_World") == "hello-world"


def test_only_hyphens():
    assert slugify("----") == ""


def test_spaces_and_underscores_mixed():
    assert slugify("a _ b") == "a-b"
