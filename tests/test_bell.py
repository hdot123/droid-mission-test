"""tests for bell.py: Bell 数验收要点逐条对应。"""

import pytest

from bell import bell_number


@pytest.mark.parametrize(
    "n,expected",
    [
        (0, 1),
        (1, 1),
        (2, 2),
        (3, 5),
        (4, 15),
        (5, 52),
        (6, 203),
        (7, 877),
        (8, 4140),
        (9, 21147),
        (10, 115975),
        (15, 1382958545),
        (20, 51724158235372),
    ],
)
def test_bell_number_values(n, expected):
    assert bell_number(n) == expected


def test_bell_number_negative_raises_value_error():
    with pytest.raises(ValueError):
        bell_number(-1)


def test_bell_number_float_raises_type_error():
    with pytest.raises(TypeError):
        bell_number(2.5)


def test_bell_number_str_raises_type_error():
    with pytest.raises(TypeError):
        bell_number("5")


def test_bell_number_bool_raises_type_error():
    with pytest.raises(TypeError):
        bell_number(True)
