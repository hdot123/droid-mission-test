"""Tests for slugtext (slugify / is_slug) only."""

from slugtext import is_slug, slugify


def test_slugify_basic_examples():
    assert slugify("Hello, World!") == "hello-world"
    assert slugify("  Python 3.12 released ") == "python-3-12-released"


def test_slugify_non_ascii_letters():
    assert slugify("Déjà vu") == "d-j-vu"


def test_slugify_empty_and_punctuation_only():
    assert slugify("") == ""
    assert slugify("!!!") == ""


def test_slugify_consecutive_separators_collapse():
    assert slugify("a  --  b") == "a-b"
    assert slugify("a___b") == "a-b"
    assert slugify("a...b") == "a-b"


def test_slugify_leading_trailing_dashes_stripped():
    assert slugify("--hello--") == "hello"
    assert slugify("-hello-") == "hello"


def test_slugify_digits_and_mixed():
    assert slugify("3.14") == "3-14"
    assert slugify("ABC123") == "abc123"


def test_is_slug_valid():
    assert is_slug("hello-world") is True
    assert is_slug("hello") is True
    assert is_slug("a-b-c") is True
    assert is_slug("abc123") is True


def test_is_slug_invalid():
    assert is_slug("Hello") is False
    assert is_slug("a--b") is False
    assert is_slug("") is False
    assert is_slug("-abc") is False
    assert is_slug("abc-") is False
    assert is_slug("a-") is False
    assert is_slug("hello world") is False
    assert is_slug("héllo") is False
