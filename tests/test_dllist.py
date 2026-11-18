"""tests/test_dllist.py: DoublyLinkedList 行为测试。"""

import pytest

from dllist import DoublyLinkedList


def test_append_order_and_len():
    dll = DoublyLinkedList()
    dll.append(1)
    dll.append(2)
    dll.append(3)
    assert dll.to_list() == [1, 2, 3]
    assert dll.to_list_reversed() == [3, 2, 1]
    assert len(dll) == 3


def test_prepend_order_and_len():
    dll = DoublyLinkedList()
    dll.append(1)
    dll.append(2)
    dll.append(3)
    dll.prepend(0)
    assert dll.to_list() == [0, 1, 2, 3]
    assert dll.to_list_reversed() == [3, 2, 1, 0]
    assert len(dll) == 4


def test_remove_first_success():
    dll = DoublyLinkedList()
    for v in (0, 1, 2, 3):
        dll.append(v)
    assert dll.remove_first(2) is True
    assert dll.to_list() == [0, 1, 3]
    assert dll.to_list_reversed() == [3, 1, 0]
    assert len(dll) == 3


def test_remove_first_absent():
    dll = DoublyLinkedList()
    for v in (0, 1, 2, 3):
        dll.append(v)
    assert dll.remove_first(9) is False
    assert dll.to_list() == [0, 1, 2, 3]
    assert len(dll) == 4


def test_remove_first_duplicates_removes_earliest():
    dll = DoublyLinkedList()
    for v in (1, 2, 1, 3):
        dll.append(v)
    assert dll.remove_first(1) is True
    assert dll.to_list() == [2, 1, 3]
    assert len(dll) == 3


def test_pop_front_back_sequence():
    dll = DoublyLinkedList()
    for v in (1, 2, 3):
        dll.append(v)
    assert dll.pop_back() == 3
    assert len(dll) == 2
    assert dll.to_list() == [1, 2]


def test_empty_pop_front_raises_index_error():
    dll = DoublyLinkedList()
    with pytest.raises(IndexError):
        dll.pop_front()


def test_empty_pop_back_raises_index_error():
    dll = DoublyLinkedList()
    with pytest.raises(IndexError):
        dll.pop_back()


def test_worked_example_full_sequence():
    dll = DoublyLinkedList()
    dll.append(1)
    dll.append(2)
    dll.append(3)
    dll.prepend(0)
    assert dll.to_list() == [0, 1, 2, 3]
    assert dll.to_list_reversed() == [3, 2, 1, 0]
    assert len(dll) == 4
    assert dll.remove_first(2) is True
    assert dll.to_list() == [0, 1, 3]
    assert dll.remove_first(9) is False
    assert dll.pop_back() == 3
    assert dll.pop_front() == 0
    assert dll.to_list() == [1]
    assert len(dll) == 1


def test_empty_list_basics():
    dll = DoublyLinkedList()
    assert len(dll) == 0
    assert dll.to_list() == []
    assert dll.to_list_reversed() == []
    assert dll.remove_first(1) is False


def test_single_element_list():
    dll = DoublyLinkedList()
    dll.append("x")
    assert len(dll) == 1
    assert dll.to_list() == ["x"]
    assert dll.to_list_reversed() == ["x"]
    assert dll.remove_first("x") is True
    assert len(dll) == 0
    assert dll.to_list() == []
