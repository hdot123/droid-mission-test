"""tests for flesch: Flesch 易读度小组件验收用例。"""

import pytest

from flesch import count_syllables, flesch_reading_ease


# ---------------------------------------------------------------------------
# count_syllables: 验收要点逐条
# ---------------------------------------------------------------------------

def test_count_syllables_cat():
    assert count_syllables("cat") == 1


def test_count_syllables_simple():
    assert count_syllables("simple") == 2


def test_count_syllables_sentence():
    assert count_syllables("sentence") == 2


def test_count_syllables_over():
    assert count_syllables("over") == 2


def test_count_syllables_lazy():
    assert count_syllables("lazy") == 2


def test_count_syllables_reading():
    assert count_syllables("reading") == 2


def test_count_syllables_opens():
    assert count_syllables("opens") == 2


def test_count_syllables_ideas():
    assert count_syllables("ideas") == 2


def test_count_syllables_different():
    assert count_syllables("different") == 3


def test_count_syllables_sundays():
    assert count_syllables("sundays") == 2


def test_count_syllables_hello():
    assert count_syllables("hello") == 2


def test_count_syllables_world():
    assert count_syllables("world") == 1


def test_count_syllables_table():
    assert count_syllables("table") == 2


def test_count_syllables_cake():
    assert count_syllables("cake") == 1


def test_count_syllables_the():
    assert count_syllables("the") == 1


def test_count_syllables_non_str_raises_type_error():
    with pytest.raises(TypeError):
        count_syllables(5)


def test_count_syllables_empty_after_strip_returns_zero():
    # 非字母字符剔除后为空 → 0
    assert count_syllables("123") == 0
    assert count_syllables("!!!") == 0


def test_count_syllables_non_ascii_stripped():
    # 非 a-z 字符剔除后按剩余字母计数
    assert count_syllables("c@t!") == 1
    assert count_syllables("ta-ble") == 2


# ---------------------------------------------------------------------------
# flesch_reading_ease: 验收要点逐条
# ---------------------------------------------------------------------------

def test_flesch_cat_sat_on_the_mat():
    assert abs(flesch_reading_ease("The cat sat on the mat.") - 116.145) < 1e-6


def test_flesch_simple_sentence():
    assert abs(flesch_reading_ease("This is a simple sentence.") - 83.32) < 1e-6


def test_flesch_quick_brown_fox():
    expected = 94.3
    assert abs(flesch_reading_ease("The quick brown fox jumps over the lazy dog.") - expected) < 1e-6


def test_flesch_reading_books_opens():
    expected = 72.61545454545457
    text = "Reading books opens the mind to new ideas and different worlds."
    assert abs(flesch_reading_ease(text) - expected) < 1e-6


def test_flesch_i_like_to_eat_cake():
    text = "I like to eat cake. It is sweet and soft. We bake it on Sundays."
    assert abs(flesch_reading_ease(text) - 111.52) < 1e-6


def test_flesch_hello_world():
    assert abs(flesch_reading_ease("Hello world") - 77.905) < 1e-6


def test_flesch_empty_raises_value_error():
    with pytest.raises(ValueError):
        flesch_reading_ease("")


def test_flesch_no_words_raises_value_error():
    with pytest.raises(ValueError):
        flesch_reading_ease("123 456")


def test_flesch_non_str_raises_type_error():
    with pytest.raises(TypeError):
        flesch_reading_ease(None)
