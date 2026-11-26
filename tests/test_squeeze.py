"""squeeze 验收测试：覆盖过程卡 887 的全部 16 个验收要点。"""

import pytest

from squeeze import squeeze_chars, squeeze_spaces


# --- squeeze_chars 验收要点 1-7 -------------------------------------------


def test_chars_empty():
    assert squeeze_chars("") == ""


def test_chars_single():
    assert squeeze_chars("a") == "a"


def test_chars_runs_collapse():
    assert squeeze_chars("aaabbbcca") == "abca"


def test_chars_no_runs():
    assert squeeze_chars("abc") == "abc"


def test_chars_digits():
    assert squeeze_chars("111222111") == "121"


def test_chars_case_sensitive():
    assert squeeze_chars("aAaA") == "aAaA"


def test_chars_unicode():
    assert squeeze_chars("αααββ") == "αβ"


# --- squeeze_spaces 验收要点 8-13 ------------------------------------------


def test_spaces_empty():
    assert squeeze_spaces("") == ""


def test_spaces_mixed_whitespace_runs():
    assert squeeze_spaces("a  b\t\tc\n\nd") == "a b c d"


def test_spaces_leading_kept_as_one_space():
    assert squeeze_spaces("  lead") == " lead"


def test_spaces_trailing_kept_as_one_space():
    assert squeeze_spaces("trail  ") == "trail "


def test_spaces_no_whitespace():
    assert squeeze_spaces("nows") == "nows"


def test_spaces_only_whitespace():
    assert squeeze_spaces("    ") == " "


# --- 验收要点 14：幂等性质 -------------------------------------------------


def test_chars_idempotent():
    for sample in ("", "a", "aaabbbcca", "abc", "111222111", "aAaA", "αααββ"):
        once = squeeze_chars(sample)
        assert squeeze_chars(once) == once


def test_spaces_idempotent():
    for sample in (
        "",
        "a  b\t\tc\n\nd",
        "  lead",
        "trail  ",
        "nows",
        "    ",
        "\t\n  mixed \t\t ends  ",
    ):
        once = squeeze_spaces(sample)
        assert squeeze_spaces(once) == once


# --- 验收要点 15-16：入参类型错误 -----------------------------------------


def test_chars_non_str_raises_type_error():
    with pytest.raises(TypeError):
        squeeze_chars(5)


def test_spaces_none_raises_type_error():
    with pytest.raises(TypeError):
        squeeze_spaces(None)


# --- 附加：两函数均对非 str 抛 TypeError ----------------------------------


@pytest.mark.parametrize("bad", [5, None, 3.5, b"abc", ["a"]])
@pytest.mark.parametrize("fn", [squeeze_chars, squeeze_spaces])
def test_both_functions_reject_non_str(fn, bad):
    with pytest.raises(TypeError):
        fn(bad)
