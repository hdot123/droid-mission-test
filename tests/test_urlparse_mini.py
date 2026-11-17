"""Tests for urlparse_mini.parse."""

import pytest

from urlparse_mini import parse


def test_spec_example_https_with_path_and_query():
    assert parse("https://example.com/a/b?x=1") == {
        "scheme": "https",
        "host": "example.com",
        "port": 443,
        "path": "/a/b",
        "query": "x=1",
    }


def test_spec_example_http_with_explicit_port():
    assert parse("http://h.io:8080") == {
        "scheme": "http",
        "host": "h.io",
        "port": 8080,
        "path": "/",
        "query": "",
    }


def test_default_port_http():
    assert parse("http://example.com")["port"] == 80


def test_default_port_https():
    assert parse("https://example.com")["port"] == 443


def test_explicit_port_overrides_default():
    assert parse("https://example.com:8443/x")["port"] == 8443


def test_missing_path_defaults_to_slash():
    assert parse("http://example.com")["path"] == "/"


def test_path_with_trailing_slash_preserved():
    assert parse("http://example.com/")["path"] == "/"


def test_empty_query_defaults_to_empty_string():
    assert parse("http://example.com/a")["query"] == ""


def test_query_without_path():
    assert parse("http://example.com?x=1") == {
        "scheme": "http",
        "host": "example.com",
        "port": 80,
        "path": "/",
        "query": "x=1",
    }


def test_query_is_raw_string():
    assert parse("http://example.com/s?b=2&a=1")["query"] == "b=2&a=1"


def test_userinfo_rejected():
    with pytest.raises(ValueError):
        parse("http://user@example.com/")


def test_fragment_rejected():
    with pytest.raises(ValueError):
        parse("https://example.com/a#frag")


def test_bad_scheme_rejected():
    with pytest.raises(ValueError):
        parse("ftp://example.com/")


def test_missing_scheme_rejected():
    with pytest.raises(ValueError):
        parse("example.com/path")


def test_empty_host_rejected():
    with pytest.raises(ValueError):
        parse("http:///path")
