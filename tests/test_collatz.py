"""Tests for the collatz module."""

import pytest

from collatz import peak, sequence, steps


def test_sequence_example():
    assert sequence(6) == [6, 3, 10, 5, 16, 8, 4, 2, 1]


def test_sequence_of_one():
    assert sequence(1) == [1]


def test_sequence_includes_start_and_ends_at_one():
    seq = sequence(7)
    assert seq[0] == 7
    assert seq[-1] == 1


def test_steps_example():
    assert steps(6) == 8


def test_peak_example():
    assert peak(6) == 16


@pytest.mark.parametrize("bad", [0, -1, -7, 1.5, 2.0, "3", None, [3]])
def test_non_positive_or_non_integer_raises(bad):
    with pytest.raises(ValueError):
        sequence(bad)
    with pytest.raises(ValueError):
        steps(bad)
    with pytest.raises(ValueError):
        peak(bad)


@pytest.mark.parametrize("n", [1, 2, 3, 6, 27])
def test_sequence_steps_peak_consistency(n):
    seq = sequence(n)
    assert seq[0] == n
    assert seq[-1] == 1
    assert steps(n) == len(seq) - 1
    assert peak(n) == max(seq)
