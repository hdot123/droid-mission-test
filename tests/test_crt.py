import pytest

from crt import crt


def test_basic_three_congruences():
    assert crt([2, 3, 2], [3, 5, 7]) == 23


def test_two_congruences():
    assert crt([1, 2], [3, 5]) == 7


def test_zero_remainders():
    assert crt([0, 0], [5, 7]) == 0


def test_congruences_mod_4_and_9():
    assert crt([3, 1], [4, 9]) == 19


def test_congruences_mod_4_and_9_second():
    assert crt([2, 3], [4, 9]) == 30


def test_single_congruence():
    assert crt([5], [7]) == 5


def test_larger_moduli():
    assert crt([10, 4, 12], [11, 13, 17]) == 2188


def test_moduli_not_coprime():
    with pytest.raises(ValueError):
        crt([1, 2], [4, 6])


def test_length_mismatch():
    with pytest.raises(ValueError):
        crt([1], [6, 7])


def test_empty_input():
    with pytest.raises(ValueError):
        crt([], [])


def test_remainder_out_of_range():
    with pytest.raises(ValueError):
        crt([5], [5])


def test_modulus_too_small():
    with pytest.raises(ValueError):
        crt([1], [1])


def test_non_int_remainder_type():
    with pytest.raises(TypeError):
        crt([1.5], [5])


def test_non_int_modulus_type():
    with pytest.raises(TypeError):
        crt([1], ["5"])


def test_container_type_errors():
    with pytest.raises(TypeError):
        crt("ab", [3, 5])
    with pytest.raises(TypeError):
        crt([1, 2], "ab")


def test_tuple_inputs_accepted():
    assert crt((2, 3, 2), (3, 5, 7)) == 23
