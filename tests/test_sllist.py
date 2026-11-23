"""Tests for sllist.SinglyLinkedList — one case per acceptance item."""

import pytest

from sllist import SinglyLinkedList


def test_constructor_from_iterable_to_list():
    assert SinglyLinkedList([1, 2, 3]).to_list() == [1, 2, 3]


def test_len_of_constructed_list():
    assert len(SinglyLinkedList([1, 2, 3])) == 3


def test_append_tail_insert():
    lst = SinglyLinkedList([1, 2, 3])
    lst.append(4)
    assert lst.to_list() == [1, 2, 3, 4]


def test_prepend_head_insert():
    lst = SinglyLinkedList([1, 2, 3, 4])
    lst.prepend(0)
    assert lst.to_list() == [0, 1, 2, 3, 4]


def test_get_first_and_last():
    lst = SinglyLinkedList([0, 1, 2, 3, 4])
    assert lst.get(0) == 0
    assert lst.get(4) == 4


def test_find_present_and_absent():
    lst = SinglyLinkedList([0, 1, 2, 3, 4])
    assert lst.find(3) == 3
    assert lst.find(99) == -1


def test_remove_existing_returns_true_and_deletes():
    lst = SinglyLinkedList([0, 1, 2, 3, 4])
    assert lst.remove(2) is True
    assert lst.to_list() == [0, 1, 3, 4]


def test_remove_missing_returns_false_and_list_unchanged():
    lst = SinglyLinkedList([0, 1, 2, 3, 4])
    assert lst.remove(99) is False
    assert lst.to_list() == [0, 1, 2, 3, 4]


def test_remove_at_returns_element_and_deletes():
    lst = SinglyLinkedList([0, 1, 3, 4])
    assert lst.remove_at(0) == 0
    assert lst.to_list() == [1, 3, 4]


def test_reverse_in_place():
    lst = SinglyLinkedList([1, 3, 4])
    lst.reverse()
    assert lst.to_list() == [4, 3, 1]


def test_clear_empties_list():
    lst = SinglyLinkedList([4, 3, 1])
    lst.clear()
    assert lst.to_list() == []
    assert len(lst) == 0


def test_empty_constructor():
    assert SinglyLinkedList().to_list() == []


def test_get_out_of_range_raises_index_error():
    lst = SinglyLinkedList([1, 2])
    with pytest.raises(IndexError):
        lst.get(2)
    with pytest.raises(IndexError):
        lst.get(-1)


def test_remove_at_out_of_range_raises_index_error():
    lst = SinglyLinkedList([1, 2])
    with pytest.raises(IndexError):
        lst.remove_at(5)


def test_get_non_int_index_raises_type_error():
    lst = SinglyLinkedList([1, 2])
    with pytest.raises(TypeError):
        lst.get(1.0)
    with pytest.raises(TypeError):
        lst.get(True)
