"""Tests for textcase: to_snake_case and to_camel_case."""

import pytest

from textcase import to_camel_case, to_snake_case


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("HelloWorld", "hello_world"),  # required camelCase example
        ("Hello World", "hello_world"),
        ("hello-world", "hello_world"),
        ("hello_world", "hello_world"),  # underscore input stays stable
        ("foo__bar", "foo_bar"),
        ("HTTPServer", "http_server"),
        ("", ""),  # empty-string edge case
    ],
)
def test_to_snake_case(raw, expected):
    assert to_snake_case(raw) == expected


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("hello_world", "helloWorld"),  # required underscore example
        ("hello world", "helloWorld"),
        ("hello-world", "helloWorld"),
        ("Hello World", "helloWorld"),
        ("a", "a"),
        ("", ""),  # empty-string edge case
    ],
)
def test_to_camel_case(raw, expected):
    assert to_camel_case(raw) == expected


def test_empty_string_returns_empty_string():
    assert to_snake_case("") == ""
    assert to_camel_case("") == ""
