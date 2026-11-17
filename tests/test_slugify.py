"""Tests for slugify module."""

from slugify import slugify


def test_basic_example():
    assert slugify("Hello, World!") == "hello-world"


def test_multiple_spaces():
    assert slugify("  A  B  ") == "a-b"


def test_empty_string():
    assert slugify("") == ""


def test_consecutive_separators():
    assert slugify("foo---bar!!baz") == "foo-bar-baz"
    assert slugify("a--b") == "a-b"
