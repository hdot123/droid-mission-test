import pytest
from fractions import Fraction

from contfrac import convergents, from_contfrac, to_contfrac


# --- to_contfrac acceptance points ---

def test_to_contfrac_415_93():
    assert to_contfrac(415, 93) == [4, 2, 6, 7]


def test_to_contfrac_355_113():
    assert to_contfrac(355, 113) == [3, 7, 16]


def test_to_contfrac_canonical_last_term_at_least_2():
    assert to_contfrac(7, 5) == [1, 2, 2]


def test_to_contfrac_floor_semantics_negative():
    # Floor division, not truncation: -7 // 5 == -2.
    assert to_contfrac(-7, 5) == [-2, 1, 1, 2]


def test_to_contfrac_zero_and_integers():
    assert to_contfrac(0, 7) == [0]
    assert to_contfrac(5, 1) == [5]
    assert to_contfrac(-3, 1) == [-3]


# --- convergents acceptance points ---

def test_convergents_415_93():
    assert convergents(415, 93) == [
        Fraction(4),
        Fraction(9, 2),
        Fraction(58, 13),
        Fraction(415, 93),
    ]


def test_convergents_last_equals_original():
    assert convergents(415, 93)[-1] == Fraction(415, 93)
    assert convergents(-7, 5)[-1] == Fraction(-7, 5)
    assert convergents(0, 7)[-1] == Fraction(0)


# --- from_contfrac acceptance points ---

def test_from_contfrac_roundtrip_examples():
    assert from_contfrac([4, 2, 6, 7]) == Fraction(415, 93)
    assert from_contfrac([-2, 1, 1, 2]) == Fraction(-7, 5)
    assert from_contfrac([0]) == 0


# --- property tests over the full grid ---

def test_properties_over_grid():
    for den in range(1, 31):
        for num in range(-60, 61):
            expected = Fraction(num, den)
            terms = to_contfrac(num, den)

            # Round trip.
            assert from_contfrac(terms) == expected

            # Canonical form: terms after the first are >= 1; last >= 2
            # whenever the expansion has more than one term.
            if len(terms) > 1:
                assert all(t >= 1 for t in terms[1:])
                assert terms[-1] >= 2

            # Convergents: last term equals the original fraction.
            convs = convergents(num, den)
            assert convs[-1] == expected
            assert len(convs) == len(terms)

            # Adjacent convergents determinant: |p_k*q_{k-1} - p_{k-1}*q_k| == 1.
            for k in range(1, len(convs)):
                prev, cur = convs[k - 1], convs[k]
                det = abs(cur.numerator * prev.denominator
                          - prev.numerator * cur.denominator)
                assert det == 1


# --- ValueError cases ---

def test_to_contfrac_invalid_denominator():
    with pytest.raises(ValueError):
        to_contfrac(1, 0)
    with pytest.raises(ValueError):
        to_contfrac(1, -3)


def test_from_contfrac_empty():
    with pytest.raises(ValueError):
        from_contfrac([])


def test_from_contfrac_terms_below_one():
    with pytest.raises(ValueError):
        from_contfrac([1, 0])
    with pytest.raises(ValueError):
        from_contfrac([1, -2])


# --- TypeError cases ---

def test_to_contfrac_non_int_inputs():
    with pytest.raises(TypeError):
        to_contfrac(1.5, 2)
    with pytest.raises(TypeError):
        to_contfrac(1, True)
    with pytest.raises(TypeError):
        to_contfrac("415", 93)
    with pytest.raises(TypeError):
        to_contfrac(415, 93.0)


def test_from_contfrac_non_int_terms():
    with pytest.raises(TypeError):
        from_contfrac([1, 2.0])
    with pytest.raises(TypeError):
        from_contfrac("12")
    with pytest.raises(TypeError):
        from_contfrac([1, True])
