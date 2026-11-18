"""Tests for slugify.slugify (this module only)."""

import slugify as slugify_module
from slugify import slugify


def test_hello_world_example():
    assert slugify("Hello World!") == "hello-world"


def test_underscores_and_spaces_example():
    assert slugify("a_b  c") == "a-b-c"


def test_lowercases_text():
    assert slugify("MiXeD Case") == "mixed-case"


def test_removes_non_alphanumeric_characters():
    assert slugify("Hello, World! (#42)") == "hello-world-42"


def test_strips_leading_and_trailing_hyphens():
    assert slugify("--hello--") == "hello"


def test_collapses_whitespace_runs_into_single_hyphen():
    assert slugify("a   b\t\nc") == "a-b-c"


def test_empty_and_symbol_only_input():
    assert slugify("") == ""
    assert slugify("!!!") == ""


def test_module_exposes_slugify_and_does_not_import_registry():
    assert slugify_module.slugify is slugify
    assert not hasattr(slugify_module, "registry")
