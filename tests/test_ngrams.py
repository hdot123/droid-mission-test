"""tests for ngrams: char_ngrams / word_ngrams（纯切分，不计数）。"""

import pytest

from ngrams import char_ngrams, word_ngrams


# --- char_ngrams 验收要点 -------------------------------------------------


def test_char_ngrams_basic_slide():
    assert char_ngrams("abcde", 2) == ["ab", "bc", "cd", "de"]


def test_char_ngrams_length_shorter_than_n_returns_empty():
    assert char_ngrams("ab", 3) == []


def test_char_ngrams_empty_text_returns_empty():
    assert char_ngrams("", 1) == []


def test_char_ngrams_unigram_is_each_char():
    assert char_ngrams("aaa", 1) == ["a", "a", "a"]


def test_char_ngrams_returns_list_of_str():
    result = char_ngrams("abc", 2)
    assert isinstance(result, list)
    assert all(isinstance(g, str) for g in result)


# --- word_ngrams 验收要点 -------------------------------------------------


def test_word_ngrams_basic_slide_returns_tuples():
    result = word_ngrams("the quick brown fox", 2)
    assert result == [("the", "quick"), ("quick", "brown"), ("brown", "fox")]
    assert all(isinstance(g, tuple) for g in result)


def test_word_ngrams_fewer_words_than_n_returns_empty():
    assert word_ngrams("one", 2) == []


def test_word_ngrams_split_absorbs_whitespace_and_tabs():
    assert word_ngrams("a  b\tc", 3) == [("a", "b", "c")]


def test_word_ngrams_unigram_yields_single_word_tuples():
    result = word_ngrams("a b c", 1)
    assert result == [("a",), ("b",), ("c",)]


def test_word_ngrams_empty_text_returns_empty():
    assert word_ngrams("", 1) == []


# --- 校验规则（两函数同） -------------------------------------------------


def test_char_ngrams_n_zero_raises_value_error():
    with pytest.raises(ValueError):
        char_ngrams("abc", 0)


def test_word_ngrams_negative_n_raises_value_error():
    with pytest.raises(ValueError):
        word_ngrams("a b", -1)


def test_char_ngrams_float_n_raises_type_error():
    with pytest.raises(TypeError):
        char_ngrams("abc", 2.0)


def test_char_ngrams_non_str_text_raises_type_error():
    with pytest.raises(TypeError):
        char_ngrams(123, 2)


def test_word_ngrams_bool_n_raises_type_error():
    # bool 是 int 的子类，必须显式拒绝
    with pytest.raises(TypeError):
        word_ngrams("a b", True)


def test_char_ngrams_bool_n_raises_type_error():
    with pytest.raises(TypeError):
        char_ngrams("abc", True)


def test_word_ngrams_non_str_text_raises_type_error():
    with pytest.raises(TypeError):
        word_ngrams(None, 1)


def test_word_ngrams_float_n_raises_type_error():
    with pytest.raises(TypeError):
        word_ngrams("a b", 2.0)


def test_validation_runs_before_slicing_window():
    # n 非法时即使文本长度不足也应先抛异常，而非返回 []
    with pytest.raises(ValueError):
        char_ngrams("a", 0)
    with pytest.raises(TypeError):
        word_ngrams("a", False)
