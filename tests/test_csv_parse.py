"""Tests for csv_parse.py."""

import pytest

from csv_parse import parse, parse_line


# --- parse_line: spec examples -------------------------------------------

def test_spec_example_quoted_fields_and_escapes():
    assert parse_line('a,"b,c","d""e"') == ["a", "b,c", 'd"e']


def test_spec_example_empty_line():
    assert parse_line("") == [""]


def test_spec_example_empty_field():
    assert parse_line("a,,c") == ["a", "", "c"]


# --- parse_line: quotes ---------------------------------------------------

def test_quoted_field_preserves_inner_commas():
    assert parse_line('"a,b",c') == ["a,b", "c"]


def test_escaped_quote_inside_quoted_field():
    assert parse_line('"d""e"') == ['d"e']
    assert parse_line('"a""b""c"') == ['a"b"c']
    # open + escaped quote + close -> a single quote character.
    assert parse_line('""""') == ['"']
    # open + escaped quote, then EOF: no closing quote -> error.
    with pytest.raises(ValueError):
        parse_line('"""')


def test_quoted_field_can_be_empty():
    assert parse_line('"",a') == ["", "a"]
    assert parse_line('a,""') == ["a", ""]


def test_unquoted_field_keeps_whitespace_verbatim():
    assert parse_line(" a , b ") == [" a ", " b "]


def test_quotes_in_middle_of_unquoted_field_are_verbatim():
    assert parse_line('a"b') == ['a"b']


def test_trailing_comma_yields_empty_final_field():
    assert parse_line("a,") == ["a", ""]
    assert parse_line('"a",') == ["a", ""]


def test_only_commas():
    assert parse_line(",") == ["", ""]


def test_unterminated_quote_raises_value_error():
    with pytest.raises(ValueError):
        parse_line('"a,b')
    with pytest.raises(ValueError):
        parse_line('a,"')


def test_non_string_input_raises_value_error():
    with pytest.raises(ValueError):
        parse_line(None)


# --- parse: multi-line ----------------------------------------------------

def test_spec_example_empty_text_returns_list():
    assert parse("") == []


def test_parse_multiple_lines():
    assert parse("a,b\nc,d") == [["a", "b"], ["c", "d"]]


def test_single_trailing_newline_is_ignored():
    assert parse("a,b\nc,d\n") == [["a", "b"], ["c", "d"]]
    assert parse("a,b\n") == [["a", "b"]]


def test_blank_interior_line_becomes_empty_field_list():
    assert parse("a\n\nb") == [["a"], [""], ["b"]]


def test_parse_quoted_commas_per_line():
    assert parse('a,"x,y"\nb') == [["a", "x,y"], ["b"]]


def test_parse_crlf_line_endings():
    assert parse("a,b\r\nc,d\r\n") == [["a", "b"], ["c", "d"]]


def test_parse_only_newline_is_empty():
    assert parse("\n") == []


def test_parse_unterminated_quote_raises_value_error():
    with pytest.raises(ValueError):
        parse('a,"b')
