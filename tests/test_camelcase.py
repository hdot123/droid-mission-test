"""Tests for camelcase (snake_case <-> camelCase) conversions."""

import pytest

from camelcase import camel_to_snake, snake_to_camel


# --- snake_to_camel acceptance points ---

def test_snake_to_camel_basic():
    assert snake_to_camel("hello_world") == "helloWorld"


def test_snake_to_camel_three_segments():
    assert snake_to_camel("hello_world_foo") == "helloWorldFoo"


def test_snake_to_camel_single_segment():
    assert snake_to_camel("hello") == "hello"


def test_snake_to_camel_single_letter_segments():
    assert snake_to_camel("a_b_c") == "aBC"


def test_snake_to_camel_trailing_underscore_raises():
    with pytest.raises(ValueError):
        snake_to_camel("hello_")


def test_snake_to_camel_uppercase_raises():
    with pytest.raises(ValueError):
        snake_to_camel("Hello_world")


def test_snake_to_camel_empty_raises():
    with pytest.raises(ValueError):
        snake_to_camel("")


# --- camel_to_snake acceptance points ---

def test_camel_to_snake_basic():
    assert camel_to_snake("helloWorld") == "hello_world"


def test_camel_to_snake_three_words():
    assert camel_to_snake("helloWorldFoo") == "hello_world_foo"


def test_camel_to_snake_leading_uppercase():
    assert camel_to_snake("HelloWorld") == "hello_world"


def test_camel_to_snake_single_word():
    assert camel_to_snake("hello") == "hello"


def test_camel_to_snake_underscore_raises():
    with pytest.raises(ValueError):
        camel_to_snake("hello_world")


def test_camel_to_snake_empty_raises():
    with pytest.raises(ValueError):
        camel_to_snake("")
