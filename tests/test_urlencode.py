"""Tests for urlencode — only exercises the urlencode module."""

import pytest

import urlencode


class TestQuote:
    def test_required_example(self):
        assert urlencode.quote("a b/中") == "a%20b/%E4%B8%AD"

    def test_unreserved_left_alone(self):
        assert urlencode.quote("AZaz09-_.~") == "AZaz09-_.~"

    def test_space_is_percent20(self):
        assert urlencode.quote(" ") == "%20"
        assert urlencode.quote("a b") == "a%20b"

    def test_default_safe_keeps_slash(self):
        assert urlencode.quote("a/b") == "a/b"

    def test_custom_safe(self):
        assert urlencode.quote("a/b?c", safe="?") == "a%2Fb?c"
        assert urlencode.quote("a/b?c", safe="/?") == "a/b?c"

    def test_safe_empty_encodes_slash(self):
        assert urlencode.quote("a/b", safe="") == "a%2Fb"

    def test_multibyte_utf8(self):
        assert urlencode.quote("é") == "%C3%A9"
        assert urlencode.quote("😀") == "%F0%9F%98%80"

    def test_empty_string(self):
        assert urlencode.quote("") == ""

    def test_reserved_chars_encoded(self):
        assert urlencode.quote("a&b=c d") == "a%26b%3Dc%20d"


class TestUnquote:
    def test_required_example(self):
        assert urlencode.unquote("a%20b%zz") == "a b%zz"

    def test_roundtrip_multibyte(self):
        assert urlencode.unquote(urlencode.quote("中")) == "中"
        assert urlencode.unquote("%E4%B8%AD") == "中"

    def test_invalid_percent_sequences_kept(self):
        assert urlencode.unquote("%zz") == "%zz"
        assert urlencode.unquote("50%") == "50%"
        assert urlencode.unquote("%a") == "%a"
        assert urlencode.unquote("100%") == "100%"

    def test_valid_sequences_mixed_with_invalid(self):
        assert urlencode.unquote("%20%zz%2") == " %zz%2"

    def test_empty_string(self):
        assert urlencode.unquote("") == ""

    def test_plain_text(self):
        assert urlencode.unquote("hello") == "hello"

    def test_invalid_utf8_raises_value_error(self):
        with pytest.raises(ValueError):
            urlencode.unquote("%FF")
        with pytest.raises(ValueError):
            urlencode.unquote("a%E0%A4")


class TestQuotePlus:
    def test_required_example(self):
        assert urlencode.quote_plus("a b") == "a+b"

    def test_default_safe_is_empty(self):
        assert urlencode.quote_plus("a/b") == "a%2Fb"

    def test_plus_is_encoded(self):
        assert urlencode.quote_plus("a+b") == "a%2Bb"

    def test_multibyte(self):
        assert urlencode.quote_plus("中 b") == "%E4%B8%AD+b"

    def test_empty_string(self):
        assert urlencode.quote_plus("") == ""


class TestUnquotePlus:
    def test_plus_becomes_space(self):
        assert urlencode.unquote_plus("a+b") == "a b"

    def test_combined_with_unquote(self):
        assert urlencode.unquote_plus("a+b%20c") == "a b c"

    def test_empty_string(self):
        assert urlencode.unquote_plus("") == ""

    def test_required_example_roundtrip(self):
        assert urlencode.unquote_plus(urlencode.quote_plus("a b")) == "a b"
