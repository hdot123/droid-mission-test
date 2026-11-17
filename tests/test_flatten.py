from flatten import flatten


def test_worked_example():
    assert flatten([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5]


def test_empty_list_returns_empty_list():
    assert flatten([]) == []


def test_non_list_elements_preserved():
    assert flatten([1, "two", 3.0, None, True]) == [1, "two", 3.0, None, True]


def test_deep_nesting_order_preservation():
    nested = [[[[[1]]], [[2, [3, [4, [5]]]]]]]
    assert flatten(nested) == [1, 2, 3, 4, 5]
    assert flatten([["a"], [[["b"]], "c"], []]) == ["a", "b", "c"]
