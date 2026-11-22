"""collatz 模块的验收测试。"""

import pytest

import collatz


def test_steps_one_is_zero():
    assert collatz.steps(1) == 0


def test_steps_six():
    assert collatz.steps(6) == 8


def test_steps_27():
    assert collatz.steps(27) == 111


def test_peak_27():
    assert collatz.peak(27) == 9232


def test_peak_one():
    assert collatz.peak(1) == 1


def test_steps_zero_raises():
    with pytest.raises(ValueError):
        collatz.steps(0)


def test_peak_negative_raises():
    with pytest.raises(ValueError):
        collatz.peak(-3)
