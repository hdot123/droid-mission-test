"""Tests for the collatz module."""

import pytest

import collatz


def test_sequence_6():
    assert collatz.sequence(6) == [6, 3, 10, 5, 16, 8, 4, 2, 1]


def test_steps_6():
    assert collatz.steps(6) == 8


def test_sequence_1():
    assert collatz.sequence(1) == [1]


def test_steps_1():
    assert collatz.steps(1) == 0


def test_steps_27():
    assert collatz.steps(27) == 111


@pytest.mark.parametrize("bad", [0, -1, 1.5, "6"])
def test_sequence_invalid_raises(bad):
    with pytest.raises(ValueError):
        collatz.sequence(bad)


@pytest.mark.parametrize("bad", [0, -1, 1.5, "6"])
def test_steps_invalid_raises(bad):
    with pytest.raises(ValueError):
        collatz.steps(bad)
