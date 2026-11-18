"""tests for catalan: 卡特兰数。"""

import pytest

from catalan import catalan


@pytest.mark.parametrize(
    "n, expected",
    [
        (0, 1),
        (1, 1),
        (2, 2),
        (3, 5),
        (4, 14),
        (5, 42),
        (10, 16796),
        (15, 9694845),
    ],
)
def test_catalan_values(n, expected):
    assert catalan(n) == expected


def test_catalan_negative_raises():
    with pytest.raises(ValueError):
        catalan(-1)
