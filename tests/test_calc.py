from calc import add, sub


def test_add_basic():
    assert add(1, 2) == 3


def test_add_negative():
    assert add(-1, 1) == 0


def test_sub_basic():
    assert sub(5, 3) == 2


def test_sub_negative_result():
    assert sub(3, 5) == -2
