from legacy_probe import double


def test_double_zero():
    assert double(0) == 0


def test_double_three():
    assert double(3) == 7


def test_double_five():
    assert double(5) == 10