"""tests/test_multiset.py — acceptance coverage for multiset.MultiSet.

Every acceptance item from the work order (sub-issue #893) has a test here.
"""

import pytest

from multiset import MultiSet


# --- construction / basic queries -------------------------------------

def test_construction_counts_and_queries():
    m = MultiSet("aabbbc")
    assert m.count("a") == 2
    assert m.count("b") == 3
    assert m.count("c") == 1
    assert m.count("z") == 0
    assert len(m) == 6
    assert m.total() == 6
    assert m.distinct() == 3
    assert "a" in m
    assert "z" not in m


def test_empty_constructors_equal():
    assert MultiSet() == MultiSet([])
    assert len(MultiSet()) == 0
    assert MultiSet().total() == 0
    assert MultiSet().distinct() == 0
    assert MultiSet().elements() == []


def test_unequal_counts_not_equal():
    assert MultiSet("ab") != MultiSet("aab")


def test_constructor_counts_in_order_for_generators():
    ms = MultiSet(ch for ch in "aab")
    assert ms.to_dict() == {"a": 2, "b": 1}
    assert ms.elements() == ["a", "a", "b"]


# --- dict / elements ----------------------------------------------------

def test_to_dict():
    assert MultiSet("aab").to_dict() == {"a": 2, "b": 1}


def test_to_dict_returns_copy():
    m = MultiSet("aab")
    d = m.to_dict()
    d["a"] = 99
    assert m.count("a") == 2


def test_elements_first_insertion_order():
    assert MultiSet("aab").elements() == ["a", "a", "b"]


def test_elements_sorted_banana():
    assert sorted(MultiSet("banana").elements()) == sorted("banana")


# --- set algebra ---------------------------------------------------------

def test_union_takes_max_and_returns_new():
    a = MultiSet("aab")
    b = MultiSet("abb")
    u = a.union(b)
    assert isinstance(u, MultiSet)
    assert u is not a and u is not b
    assert u.to_dict() == {"a": 2, "b": 2}
    assert a.to_dict() == {"a": 2, "b": 1}
    assert b.to_dict() == {"a": 1, "b": 2}


def test_intersection_takes_min_and_returns_new():
    a = MultiSet("aab")
    b = MultiSet("abb")
    i = a.intersection(b)
    assert isinstance(i, MultiSet)
    assert i is not a and i is not b
    assert i.to_dict() == {"a": 1, "b": 1}
    assert a.to_dict() == {"a": 2, "b": 1}
    assert b.to_dict() == {"a": 1, "b": 2}


def test_difference_both_directions_and_returns_new():
    a = MultiSet("aab")
    b = MultiSet("abb")
    d1 = a.difference(b)
    d2 = b.difference(a)
    assert isinstance(d1, MultiSet) and isinstance(d2, MultiSet)
    assert d1 is not a and d2 is not b
    assert d1.to_dict() == {"a": 1}
    assert d2.to_dict() == {"b": 1}
    assert a.to_dict() == {"a": 2, "b": 1}
    assert b.to_dict() == {"a": 1, "b": 2}


def test_difference_drops_zero_counts():
    assert MultiSet("aab").difference(MultiSet("aab")).to_dict() == {}
    assert MultiSet("ab").difference(MultiSet("aa")).to_dict() == {"b": 1}


def test_union_disjoint_items():
    assert MultiSet("a").union(MultiSet("b")).to_dict() == {"a": 1, "b": 1}


def test_is_subset_both_directions():
    a = MultiSet("aab")
    assert MultiSet("ab").is_subset(a) is True
    assert a.is_subset(MultiSet("ab")) is False
    assert a.is_subset(MultiSet("aab")) is True


# --- equality against non-MultiSet --------------------------------------

def test_equality_with_plain_dict_is_false():
    assert (MultiSet("ab") == {"a": 1, "b": 1}) is False
    assert (MultiSet("ab") != {"a": 1, "b": 1}) is True


# --- add / remove lifecycle ----------------------------------------------

def test_add_then_partial_remove_keeps_count():
    m2 = MultiSet()
    m2.add("x", 3)
    m2.remove("x", 2)
    assert m2.count("x") == 1
    assert len(m2) == 1


def test_remove_to_zero_deletes_item():
    m2 = MultiSet()
    m2.add("x", 3)
    m2.remove("x", 2)
    m2.remove("x")
    assert "x" not in m2
    assert m2.distinct() == 0
    assert m2.total() == 0


def test_add_appends_in_insertion_order():
    m = MultiSet("a")
    m.add("b")
    m.add("a")
    assert m.elements() == ["a", "a", "b"]
    assert m.to_dict() == {"a": 2, "b": 1}


def test_remove_reinsert_keeps_first_insertion_slot():
    m = MultiSet("ab")
    m.remove("a")
    m.add("a")
    assert m.elements() == ["b", "a"]


# --- ValueError cases -----------------------------------------------------

def test_remove_more_than_held_raises_value_error():
    with pytest.raises(ValueError):
        MultiSet("ab").remove("a", 2)


def test_remove_missing_item_raises_value_error():
    with pytest.raises(ValueError):
        MultiSet().remove("ghost")


def test_add_zero_raises_value_error():
    with pytest.raises(ValueError):
        MultiSet().add("x", 0)


def test_add_negative_raises_value_error():
    with pytest.raises(ValueError):
        MultiSet().add("x", -1)


def test_remove_zero_n_raises_value_error():
    with pytest.raises(ValueError):
        MultiSet("a").remove("a", 0)


# --- TypeError cases ------------------------------------------------------

def test_add_float_n_raises_type_error():
    with pytest.raises(TypeError):
        MultiSet().add("x", 1.5)


def test_add_bool_n_raises_type_error():
    with pytest.raises(TypeError):
        MultiSet().add("x", True)


def test_remove_non_int_n_raises_type_error():
    with pytest.raises(TypeError):
        MultiSet("a").remove("a", 1.5)
    with pytest.raises(TypeError):
        MultiSet("a").remove("a", True)
