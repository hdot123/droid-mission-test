"""原版 Jaro（不含 Winkler）验收测试——覆盖工单 #890 全部验收要点。"""

import pytest

from jaro import jaro_similarity

REL = 1e-9


def test_martha_marhta():
    assert jaro_similarity("MARTHA", "MARHTA") == pytest.approx(
        0.9444444444, rel=REL
    )


def test_dwayne_duane_is_original_jaro_not_winkler():
    value = jaro_similarity("DWAYNE", "DUANE")
    assert value == pytest.approx(0.8222222222, rel=REL)
    # 头号陷阱：教科书流传的 0.84 是 Jaro–Winkler 值，本题不收。
    assert value != pytest.approx(0.84, rel=REL)


def test_dixon_dicksonx_is_original_jaro_not_winkler():
    value = jaro_similarity("DIXON", "DICKSONX")
    assert value == pytest.approx(0.7666666667, rel=REL)
    # 头号陷阱：教科书流传的 0.8133 是 Jaro–Winkler 值，本题不收。
    assert value != pytest.approx(0.8133, rel=REL)


def test_crate_trace():
    assert jaro_similarity("CRATE", "TRACE") == pytest.approx(
        0.7333333333, rel=REL
    )


def test_empty_strings():
    assert jaro_similarity("", "") == 1.0
    assert jaro_similarity("a", "") == 0.0
    assert jaro_similarity("", "a") == 0.0


def test_identical_strings():
    assert jaro_similarity("abc", "abc") == 1.0
    assert jaro_similarity("a", "a") == 1.0


def test_disjoint_strings():
    assert jaro_similarity("abc", "xyz") == 0.0
    assert jaro_similarity("a", "b") == 0.0


def test_zero_window_no_crossing_match():
    # 匹配窗 = max(2, 2) // 2 - 1 = 0：只看对角线，"ab"/"ba" 无匹配。
    assert jaro_similarity("ab", "ba") == 0.0


_PAIRS = [
    ("MARTHA", "MARHTA"),
    ("DWAYNE", "DUANE"),
    ("DIXON", "DICKSONX"),
    ("CRATE", "TRACE"),
    ("", ""),
    ("a", ""),
    ("", "a"),
    ("abc", "abc"),
    ("abc", "xyz"),
    ("a", "a"),
    ("a", "b"),
    ("ab", "ba"),
    ("banana", "anabana"),
    ("hello", "hallo"),
    ("the quick brown fox", "the quick brown fox"),
    ("prefix", "suffix"),
    ("1234567890", "abcdefghij"),
]


def test_symmetric():
    for a, b in _PAIRS:
        forward = jaro_similarity(a, b)
        backward = jaro_similarity(b, a)
        assert forward == pytest.approx(backward, rel=REL, abs=1e-12)


def test_value_always_in_unit_interval():
    for a, b in _PAIRS:
        value = jaro_similarity(a, b)
        assert 0.0 <= value <= 1.0


def test_non_string_arguments_raise_type_error():
    with pytest.raises(TypeError):
        jaro_similarity("a", 1)
    with pytest.raises(TypeError):
        jaro_similarity(None, "a")
    with pytest.raises(TypeError):
        jaro_similarity(1, "a")
    with pytest.raises(TypeError):
        jaro_similarity(b"a", "a")
    with pytest.raises(TypeError):
        jaro_similarity(True, "a")
