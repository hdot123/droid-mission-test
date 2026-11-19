"""Tests for ringbuffer.RingBuffer — fixed-capacity ring buffer."""

import pytest

from ringbuffer import RingBuffer


def test_fresh_buffer_empty_not_full():
    rb = RingBuffer(3)
    assert rb.is_empty() is True
    assert rb.is_full() is False


def test_fill_to_capacity():
    rb = RingBuffer(3)
    rb.append(1)
    rb.append(2)
    rb.append(3)
    assert rb.to_list() == [1, 2, 3]
    assert len(rb) == 3
    assert rb.is_full() is True
    assert rb.is_empty() is False


def test_overwrite_one_keeps_order():
    rb = RingBuffer(3)
    for value in (1, 2, 3, 4):
        rb.append(value)
    assert rb.to_list() == [2, 3, 4]


def test_overwrite_multiple():
    rb = RingBuffer(3)
    for value in (1, 2, 3, 4, 5, 6):
        rb.append(value)
    assert rb.to_list() == [4, 5, 6]
    assert len(rb) == 3


def test_iterate_oldest_to_newest():
    rb = RingBuffer(3)
    for value in (1, 2, 3, 4, 5, 6):
        rb.append(value)
    assert list(rb) == [4, 5, 6]


def test_capacity_one():
    rb = RingBuffer(1)
    rb.append("a")
    assert rb.to_list() == ["a"]
    rb.append("b")
    assert rb.to_list() == ["b"]
    assert len(rb) == 1


def test_can_store_none():
    rb = RingBuffer(2)
    rb.append(None)
    assert rb.to_list() == [None]
    assert len(rb) == 1


def test_zero_capacity_raises_value_error():
    with pytest.raises(ValueError):
        RingBuffer(0)


def test_negative_capacity_raises_value_error():
    with pytest.raises(ValueError):
        RingBuffer(-2)


def test_float_capacity_raises_type_error():
    with pytest.raises(TypeError):
        RingBuffer(2.5)


def test_str_capacity_raises_type_error():
    with pytest.raises(TypeError):
        RingBuffer("3")
