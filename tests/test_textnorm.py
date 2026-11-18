"""Tests for textnorm.normalize — only exercises the textnorm module."""

import textnorm


def test_lowercase():
    assert textnorm.normalize("HELLO World") == "hello world"


def test_delete_non_alphanumeric_non_whitespace():
    assert textnorm.normalize("a,b!c;d:e") == "abcde"
    # apostrophe removed, so "It's" becomes "its"
    assert textnorm.normalize("It's") == "its"


def test_collapse_whitespace():
    assert textnorm.normalize("a   b\tc\nd") == "a b c d"


def test_strip_ends():
    assert textnorm.normalize("   hi   ") == "hi"


def test_spec_example():
    assert textnorm.normalize("  Hello,   World!\nIt's 2026. ") == "hello world its 2026"
