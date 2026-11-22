"""deltaenc 的验收测试（第四十五轮 · 并发 C 单）。"""

import pytest

from deltaenc import delta_decode, delta_encode


def test_encode_basic():
    assert delta_encode([10, 12, 15, 15, 20]) == [10, 2, 3, 0, 5]


def test_decode_basic():
    assert delta_decode([10, 2, 3, 0, 5]) == [10, 12, 15, 15, 20]


def test_encode_empty():
    assert delta_encode([]) == []


def test_decode_empty():
    assert delta_decode([]) == []


def test_encode_single():
    assert delta_encode([7]) == [7]


def test_decode_single():
    assert delta_decode([7]) == [7]


def test_encode_with_zero_and_negative_delta():
    assert delta_encode([5, 3, 3, 10]) == [5, -2, 0, 7]


def test_decode_with_zero_and_negative_delta():
    assert delta_decode([5, -2, 0, 7]) == [5, 3, 3, 10]


def test_encode_negative_values():
    assert delta_encode([-5, -3, -10]) == [-5, 2, -7]


def test_decode_negative_values():
    assert delta_decode([-5, 2, -7]) == [-5, -3, -10]


def test_encode_all_zeros():
    assert delta_encode([0, 0, 0]) == [0, 0, 0]


def test_encode_large_values():
    assert delta_encode([1000000, 999999, 1000001]) == [1000000, -1, 2]


@pytest.mark.parametrize(
    "seq",
    [
        [3, 1, 4, 1, 5, 9, 2, 6],
        [0],
        [-1, -2, -3],
        [100, 200, 150, 150, 151],
    ],
)
def test_roundtrip(seq):
    assert delta_decode(delta_encode(seq)) == seq


def test_encode_non_list_raises():
    with pytest.raises(TypeError):
        delta_encode((1, 2))


def test_encode_non_int_element_raises():
    with pytest.raises(TypeError):
        delta_encode([1, 2.5])


def test_encode_bool_element_raises():
    with pytest.raises(TypeError):
        delta_encode([1, True])


def test_decode_non_list_raises():
    with pytest.raises(TypeError):
        delta_decode("abc")


def test_decode_non_int_element_raises():
    with pytest.raises(TypeError):
        delta_decode([1, 0.5])
