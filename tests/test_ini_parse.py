"""Tests for the ini_parse module only."""

import pytest

import ini_parse


def test_empty_text_returns_empty_dict():
    assert ini_parse.parse("") == {}


def test_ignores_leading_trailing_whitespace_and_blank_lines():
    assert ini_parse.parse("  \n\n   \n") == {}


def test_full_line_comments_ignored():
    text = "; comment\n# another comment\n[s]\n; inside\nk = v\n"
    assert ini_parse.parse(text) == {"s": {"k": "v"}}


def test_section_header_name_stripped_and_case_sensitive():
    assert ini_parse.parse("  [ Name ]  \nk = v\n") == {"Name": {"k": "v"}}
    assert ini_parse.parse("[A]\nk = v\n") != ini_parse.parse("[a]\nk = v\n")


def test_key_value_equals_and_colon():
    assert ini_parse.parse("[s]\nk = v\nj: w\n") == {"s": {"k": "v", "j": "w"}}


def test_key_stripped_and_lowercased_value_stripped():
    assert ini_parse.parse("[s]\n  Key   =   val  \n") == {"s": {"key": "val"}}


def test_keys_before_section_go_to_default():
    assert ini_parse.parse("k = v\n[s]\nk = w\n") == {
        "DEFAULT": {"k": "v"},
        "s": {"k": "w"},
    }


def test_repeated_key_in_same_section_overwrites():
    assert ini_parse.parse("[a]\nX = 1\nx = 2\n") == {"a": {"x": "2"}}


def test_repeated_section_header_merges():
    text = "[s]\na = 1\n[t]\nb = 2\n[s]\nc = 3\n"
    assert ini_parse.parse(text) == {"s": {"a": "1", "c": "3"}, "t": {"b": "2"}}


def test_matching_double_quotes_stripped_without_escape_processing():
    assert ini_parse.parse('[s]\nq = "a b"\n') == {"s": {"q": "a b"}}
    # No escape processing: backslash stays literal, quotes kept when unbalanced.
    assert ini_parse.parse('[s]\nq = "a\\"b"\n') == {"s": {'q': 'a\\"b'}}
    assert ini_parse.parse('[s]\nq = "unbalanced\n') == {"s": {"q": '"unbalanced'}}
    assert ini_parse.parse('[s]\nq = ab"\n') == {"s": {"q": 'ab"'}}


def test_invalid_line_raises_value_error_with_line_number():
    with pytest.raises(ValueError) as excinfo:
        ini_parse.parse("[s]\nok = 1\nbad line here\n")
    assert "3" in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        ini_parse.parse("only text\n")
    assert "1" in str(excinfo.value)


def test_example_parse_a():
    assert ini_parse.parse("[a]\nX = 1\nx = 2\n") == {"a": {"x": "2"}}


def test_example_parse_default_and_section():
    assert ini_parse.parse("k = v\n[s]\nk = w\n") == {
        "DEFAULT": {"k": "v"},
        "s": {"k": "w"},
    }


def test_example_parse_quoted_value():
    assert ini_parse.parse('[s]\nq = "a b"\n') == {"s": {"q": "a b"}}


def test_get_basic_and_default():
    assert ini_parse.get("k = v", "DEFAULT", "K") == "v"
    assert ini_parse.get("[s]\nk = v\n", "s", "k") == "v"


def test_get_section_case_sensitive():
    assert ini_parse.get("[s]\nk = v\n", "S", "k", "missing") == "missing"


def test_get_key_case_insensitive():
    assert ini_parse.get("[s]\nKey = v\n", "s", "KEY") == "v"


def test_get_returns_default_when_missing():
    assert ini_parse.get("[s]\nk = v\n", "s", "nope") is None
    assert ini_parse.get("[s]\nk = v\n", "s", "nope", "fallback") == "fallback"
    assert ini_parse.get("[s]\nk = v\n", "other", "k", "fallback") == "fallback"
    assert ini_parse.get("", "s", "k", "fallback") == "fallback"
