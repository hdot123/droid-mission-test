"""Tests for the Stack module (stack.py)."""

import pytest

from stack import Stack


def test_body_example():
    s = Stack()
    s.push(1)
    s.push(2)
    assert s.pop() == 2
    assert s.peek() == 1
    assert s.size() == 1


def test_push_and_pop_lifo_order():
    s = Stack()
    s.push("a")
    s.push("b")
    s.push("c")
    assert s.pop() == "c"
    assert s.pop() == "b"
    assert s.pop() == "a"
    assert s.is_empty()
    assert s.size() == 0


def test_peek_does_not_remove():
    s = Stack()
    s.push(1)
    s.push(2)
    assert s.peek() == 2
    assert s.size() == 2
    assert s.peek() == 2


def test_is_empty():
    s = Stack()
    assert s.is_empty() is True
    s.push(1)
    assert s.is_empty() is False
    s.pop()
    assert s.is_empty() is True


def test_size():
    s = Stack()
    assert s.size() == 0
    s.push(1)
    assert s.size() == 1
    s.push(2)
    assert s.size() == 2
    s.pop()
    assert s.size() == 1


def test_pop_empty_raises_index_error():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()


def test_peek_empty_raises_index_error():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()
