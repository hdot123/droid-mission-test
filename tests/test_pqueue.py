"""Tests for the PriorityQueue module."""

import pytest

from pqueue import PriorityQueue


def test_worked_example():
    q = PriorityQueue()
    q.push("a", 2)
    q.push("b", 1)
    q.push("c", 1)
    assert q.peek() == "b"
    assert len(q) == 3
    assert q.pop() == "b"
    assert q.pop() == "c"
    assert q.pop() == "a"
    assert q.is_empty() is True


def test_min_priority_ordering():
    q = PriorityQueue()
    q.push("low", 10)
    q.push("high", 0)
    q.push("mid", 5)
    assert q.pop() == "high"
    assert q.pop() == "mid"
    assert q.pop() == "low"


def test_fifo_tie_breaking():
    q = PriorityQueue()
    for item in ["first", "second", "third", "fourth"]:
        q.push(item, 7)
    assert q.pop() == "first"
    assert q.pop() == "second"
    assert q.pop() == "third"
    assert q.pop() == "fourth"


def test_tie_breaking_with_mixed_priorities():
    q = PriorityQueue()
    q.push("a1", 1)
    q.push("a2", 1)
    q.push("b", 2)
    q.push("c", 0)
    assert q.pop() == "c"
    assert q.pop() == "a1"
    assert q.pop() == "a2"
    assert q.pop() == "b"


def test_peek_does_not_remove():
    q = PriorityQueue()
    q.push("only", 3)
    assert q.peek() == "only"
    assert q.peek() == "only"
    assert len(q) == 1
    assert q.is_empty() is False
    assert q.pop() == "only"


def test_empty_pop_raises_index_error():
    q = PriorityQueue()
    with pytest.raises(IndexError):
        q.pop()


def test_empty_peek_raises_index_error():
    q = PriorityQueue()
    with pytest.raises(IndexError):
        q.peek()


def test_len_and_is_empty():
    q = PriorityQueue()
    assert len(q) == 0
    assert q.is_empty() is True
    q.push("x", 1)
    assert len(q) == 1
    assert q.is_empty() is False
    q.push("y", 2)
    assert len(q) == 2
    q.pop()
    assert len(q) == 1
    assert q.is_empty() is False
    q.pop()
    assert len(q) == 0
    assert q.is_empty() is True


def test_items_need_not_be_comparable():
    q = PriorityQueue()
    q.push({"b": 1}, 2)
    q.push([1, 2], 1)
    q.push((3,), 1)
    first = q.pop()
    assert first == [1, 2]
    second = q.pop()
    assert second == (3,)
    third = q.pop()
    assert third == {"b": 1}


def test_negative_and_float_priorities():
    q = PriorityQueue()
    q.push("zero", 0.0)
    q.push("neg", -1.5)
    q.push("pos", 2)
    assert q.pop() == "neg"
    assert q.pop() == "zero"
    assert q.pop() == "pos"


def test_none_item_allowed():
    q = PriorityQueue()
    q.push(None, 1)
    q.push("other", 0)
    assert q.pop() == "other"
    assert q.pop() is None
