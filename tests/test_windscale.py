"""tests/test_windscale.py: 蒲福风级组件验收测试。"""

import pytest

from windscale import beaufort, beaufort_label


@pytest.mark.parametrize(
    "speed,expected",
    [
        (0, 0),
        (0.9, 0),
        (1, 1),
        (5, 1),
        (6, 2),
        (11, 2),
        (12, 3),
        (19, 3),
        (20, 4),
        (28, 4),
        (29, 5),
        (38, 5),
        (39, 6),
        (49, 6),
        (50, 7),
        (61, 7),
        (62, 8),
        (74, 8),
        (75, 9),
        (88, 9),
        (89, 10),
        (102, 10),
        (103, 11),
        (117, 11),
        (118, 12),
        (200, 12),
        (32.5, 5),
    ],
)
def test_beaufort_levels(speed, expected):
    assert beaufort(speed) == expected


@pytest.mark.parametrize(
    "speed,expected",
    [
        (0, "无风"),
        (3, "软风"),
        (30, "清风"),
        (55, "疾风"),
        (100, "狂风"),
        (118, "飓风"),
    ],
)
def test_beaufort_label(speed, expected):
    assert beaufort_label(speed) == expected


def test_beaufort_negative_raises_value_error():
    with pytest.raises(ValueError):
        beaufort(-1)


@pytest.mark.parametrize("bad", ["50", True, None])
def test_beaufort_type_errors(bad):
    with pytest.raises(TypeError):
        beaufort(bad)


def test_beaufort_label_negative_raises_value_error():
    with pytest.raises(ValueError):
        beaufort_label(-1)


@pytest.mark.parametrize("bad", ["50", True, None])
def test_beaufort_label_type_errors(bad):
    with pytest.raises(TypeError):
        beaufort_label(bad)
