import pytest

from fib import fib, fib_list


def test_fib_zero():
    assert fib(0) == 0


def test_fib_one():
    assert fib(1) == 1


def test_fib_two():
    assert fib(2) == 1


def test_fib_ten():
    assert fib(10) == 55


def test_fib_twenty():
    assert fib(20) == 6765


def test_fib_fifty():
    assert fib(50) == 12586269025


def test_fib_negative_raises():
    with pytest.raises(ValueError):
        fib(-1)


def test_fib_list_six():
    assert fib_list(6) == [0, 1, 1, 2, 3, 5]


def test_fib_list_one():
    assert fib_list(1) == [0]


def test_fib_list_zero():
    assert fib_list(0) == []


def test_fib_list_negative_raises():
    with pytest.raises(ValueError):
        fib_list(-1)
