import pytest

from primorial import primorial


def test_primorial_zero():
    assert primorial(0) == 1


def test_primorial_one():
    assert primorial(1) == 2


def test_primorial_two():
    assert primorial(2) == 6


def test_primorial_three():
    assert primorial(3) == 30


def test_primorial_four():
    assert primorial(4) == 210


def test_primorial_five():
    assert primorial(5) == 2310


def test_primorial_six():
    assert primorial(6) == 30030


def test_primorial_seven():
    assert primorial(7) == 510510


def test_primorial_eight():
    assert primorial(8) == 9699690


def test_primorial_nine():
    assert primorial(9) == 223092870


def test_primorial_ten():
    assert primorial(10) == 6469693230


def test_primorial_ratio():
    assert primorial(6) // primorial(5) == 13


def test_primorial_negative_raises():
    with pytest.raises(ValueError):
        primorial(-1)


def test_primorial_float_raises():
    with pytest.raises(TypeError):
        primorial(3.0)


def test_primorial_bool_raises():
    with pytest.raises(TypeError):
        primorial(True)
