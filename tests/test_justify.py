"""tests/test_justify.py: justify.py（文本两端对齐）验收测试。

覆盖第57轮 A 单 justify 逐条验收要点（逐字为准）。
"""

import pytest

from justify import justify_text


# ---------------------------------------------------------------- 逐字验收要点

def test_example_16():
    assert justify_text("This is an example of text justification.", 16) == [
        "This    is    an",
        "example  of text",
        "justification.",
    ]


def test_empty_text_returns_empty_list():
    assert justify_text("", 10) == []


def test_whitespace_only_returns_empty_list():
    assert justify_text("   ", 10) == []


def test_single_word_not_justified():
    assert justify_text("hello", 10) == ["hello"]


def test_greedy_break_a_b_c_width_3():
    assert justify_text("a b c", 3) == ["a b", "c"]


def test_overlong_word_owns_line_verbatim():
    assert justify_text("aaa bbbbbbbbbb cc", 5) == ["aaa", "bbbbbbbbbb", "cc"]


# ---------------------------------------------------------------- 性质测试

def test_property_word_order_preserved():
    text = "The quick brown fox jumps over the lazy dog right now"
    for width in range(3, 25):
        lines = justify_text(text, width)
        rejoined = [w for line in lines for w in line.split()]
        assert rejoined == text.split()


def test_property_non_last_multiword_lines_exact_width():
    text = "This is an example of text justification on a wide range of inputs"
    for width in range(3, 30):
        lines = justify_text(text, width)
        for line in lines[:-1]:
            if len(line.split()) > 1:
                assert len(line) == width


def test_property_last_line_single_spaces():
    text = "supercalifragilistic expialidocious words keep flowing here today"
    for width in range(4, 20):
        lines = justify_text(text, width)
        assert lines[-1] == " ".join(text.split()[-len(lines[-1].split()):])
        # 末行是单空格连接：不含连续双空格
        assert "  " not in lines[-1]


def test_property_remainder_spaces_left_to_right():
    # 行 "aa bb cc" 6 字符 + 2 个间隙，width 9 需 3 空格：均分 1/1 余 1 给最左隙 -> [2, 1]
    assert justify_text("aa bb cc dd", 9) == ["aa  bb cc", "dd"]


def test_property_even_split_when_no_remainder():
    # 行 "ab cd ef" 6 字符 + 2 个间隙，width 16 需 10 空格：无余数 -> [5, 5]
    assert justify_text("ab cd ef longword", 16) == ["ab     cd     ef", "longword"]


# ---------------------------------------------------------------- 入参约定

def test_width_zero_raises_value_error():
    with pytest.raises(ValueError):
        justify_text("a b", 0)


def test_negative_width_raises_value_error():
    with pytest.raises(ValueError):
        justify_text("a b", -1)


def test_non_str_text_raises_type_error():
    with pytest.raises(TypeError):
        justify_text(12, 5)


def test_float_width_raises_type_error():
    with pytest.raises(TypeError):
        justify_text("a b", 2.5)


def test_bool_width_raises_type_error():
    with pytest.raises(TypeError):
        justify_text("a b", True)
