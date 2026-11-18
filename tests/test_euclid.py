from euclid import gcd, is_coprime, lcm


def test_gcd_basic():
    assert gcd(48, 36) == 12


def test_gcd_negative_input():
    assert gcd(-48, 36) == 12


def test_gcd_with_zero():
    assert gcd(0, 5) == 5


def test_gcd_zero_zero():
    assert gcd(0, 0) == 0


def test_gcd_coprime():
    assert gcd(17, 5) == 1


def test_lcm_basic():
    assert lcm(4, 6) == 12


def test_lcm_zero():
    assert lcm(0, 7) == 0


def test_lcm_negative_input():
    assert lcm(-4, 6) == 12


def test_is_coprime_true():
    assert is_coprime(8, 9) is True


def test_is_coprime_false():
    assert is_coprime(8, 12) is False
