"""lexer.tokenize 的行为测试（只测 lexer 自身）。"""

import lexer


def test_lowercase_unified():
    assert lexer.tokenize("The CAT") == ["the", "cat"]


def test_whitespace_splitting():
    assert lexer.tokenize("a\tb\n c") == ["a", "b", "c"]


def test_punctuation_stripped_both_ends():
    assert lexer.tokenize('"hello," world!') == ["hello", "world"]


def test_punctuation_only_token_dropped():
    assert lexer.tokenize("... !!! ( )") == []


def test_empty_text():
    assert lexer.tokenize("") == []


def test_worked_example():
    assert lexer.tokenize("The cat, the CAT.") == ["the", "cat", "the", "cat"]
