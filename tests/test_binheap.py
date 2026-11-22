import random

import pytest

from binheap import BinHeap


def _filled():
    heap = BinHeap()
    for value in (5, 3, 8, 1, 9, 2):
        heap.push(value)
    return heap


def test_len_after_six_pushes():
    assert len(_filled()) == 6


def test_peek_is_smallest():
    assert _filled().peek() == 1


def test_pop_returns_smallest_then_next_peek():
    heap = _filled()
    assert heap.pop() == 1
    assert heap.peek() == 2


def test_successive_pops_yield_sorted_order():
    heap = _filled()
    assert heap.pop() == 1
    assert heap.pop() == 2
    assert heap.pop() == 3
    assert heap.pop() == 5
    assert heap.pop() == 8
    assert heap.pop() == 9


def test_is_empty_after_full_drain():
    heap = _filled()
    while not heap.is_empty():
        heap.pop()
    assert heap.is_empty() is True


def test_empty_heap_is_empty():
    heap = BinHeap()
    assert heap.is_empty() is True
    assert len(heap) == 0


def test_empty_pop_raises_index_error():
    with pytest.raises(IndexError):
        BinHeap().pop()


def test_empty_peek_raises_index_error():
    with pytest.raises(IndexError):
        BinHeap().peek()


def test_duplicate_values_allowed():
    heap = BinHeap()
    for _ in range(3):
        heap.push(4)
    assert len(heap) == 3
    assert [heap.pop() for _ in range(3)] == [4, 4, 4]


def test_push_string_raises_type_error():
    with pytest.raises(TypeError):
        BinHeap().push("a")


def test_push_bool_raises_type_error():
    heap = BinHeap()
    with pytest.raises(TypeError):
        heap.push(True)
    with pytest.raises(TypeError):
        heap.push(False)
    assert heap.is_empty() is True


def test_push_other_non_numeric_raises_type_error():
    heap = BinHeap()
    for bad in (None, [1], (1,), {"a": 1}):
        with pytest.raises(TypeError):
            heap.push(bad)
    assert heap.is_empty() is True


def test_push_accepts_negative_and_float_values():
    heap = BinHeap()
    for value in (-3, 2.5, -10, 0):
        heap.push(value)
    assert heap.pop() == -10
    assert heap.pop() == -3
    assert heap.pop() == 0
    assert heap.pop() == 2.5


def test_random_insert_order_yields_sorted_drain():
    random.seed(44)
    values = [random.randint(-50, 50) for _ in range(50)]
    heap = BinHeap()
    for value in values:
        heap.push(value)
    drained = []
    while not heap.is_empty():
        drained.append(heap.pop())
    assert drained == sorted(values)
    assert heap.is_empty() is True


def test_peek_does_not_remove():
    heap = BinHeap()
    heap.push(7)
    assert heap.peek() == 7
    assert heap.peek() == 7
    assert len(heap) == 1
    assert heap.pop() == 7
    assert heap.is_empty() is True


def test_len_tracks_push_and_pop():
    heap = BinHeap()
    assert len(heap) == 0
    heap.push(1)
    heap.push(2)
    assert len(heap) == 2
    heap.pop()
    assert len(heap) == 1
    heap.pop()
    assert len(heap) == 0
