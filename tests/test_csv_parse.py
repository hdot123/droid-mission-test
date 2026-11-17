"""Tests for csv_parse: RFC 4180 subset parser."""

import pytest

import csv_parse


# --- parse_line: required examples ---

def test_parse_line_mixed_quotes_example():
    assert csv_parse.parse_line('a,"b,c","d""e"') == ["a", "b,c", 'd"e']


def test_parse_line_empty_string_returns_empty_field():
    assert csv_parse.parse_line("") == [""]


def test_parse_line_empty_fields_between_commas():
    assert csv_parse.parse_line("a,,c") == ["a", "", "c"]


# --- parse_line: quoting rules ---

def test_parse_line_quoted_field_keeps_comma():
    assert csv_parse.parse_line('"one,two"') == ["one,two"]


def test_parse_line_doubled_quote_is_escaped_quote():
    assert csv_parse.parse_line('"a""b"') == ['a"b']


def test_parse_line_quoted_field_containing_spaces_preserved_verbatim():
    assert csv_parse.parse_line('"  spaced  "') == ["  spaced  "]


def test_parse_line_field_outside_quotes_keeps_whitespace():
    assert csv_parse.parse_line("  a , b  ,c") == ["  a ", " b  ", "c"]


def test_parse_line_unclosed_quote_raises_value_error():
    with pytest.raises(ValueError):
        csv_parse.parse_line('a,"unclosed')


def test_parse_line_unclosed_quote_only_quote_raises():
    with pytest.raises(ValueError):
        csv_parse.parse_line('"')


def test_parse_line_quoted_empty_field():
    assert csv_parse.parse_line('"",x') == ["", "x"]


def test_parse_line_consecutive_quoted_fields():
    assert csv_parse.parse_line('"a","b","c"') == ["a", "b", "c"]


def test_parse_line_single_field_no_commas():
    assert csv_parse.parse_line("plain") == ["plain"]


# --- parse: multi-line behavior ---

def test_parse_empty_text_returns_empty_list():
    assert csv_parse.parse("") == []


def test_parse_single_trailing_newline_not_producing_trailing_empty_row():
    assert csv_parse.parse('a,b\n') == [["a", "b"]]


def test_parse_multi_line_text():
    text = 'name,note\n"alice","x,y"\nbob,ok\n'
    assert csv_parse.parse(text) == [
        ["name", "note"],
        ["alice", "x,y"],
        ["bob", "ok"],
    ]


def test_parse_without_trailing_newline():
    assert csv_parse.parse("a,b\nc,d") == [["a", "b"], ["c", "d"]]


def test_parse_empty_line_in_middle_yields_empty_field_row():
    assert csv_parse.parse("a\n\nb") == [["a"], [""], ["b"]]
