"""Tests for rot13.apply."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rot13 import apply


def test_simple_word():
    assert apply("abc") == "nop"


def test_case_preserved():
    assert apply("AbC") == "NoP"


def test_non_letter_characters_preserved():
    assert apply("a1! b2?") == "n1! o2?"


def test_punctuation_digits_spaces_unchanged():
    text = "Hello, World! 123"
    # Letters shift; comma, exclamation, digits, spaces stay put.
    assert apply(text) == "Uryyb, Jbeyq! 123"


def test_round_trip_example():
    original = "Hello, World!"
    assert apply(apply(original)) == original


def test_involution_on_mixed_string():
    mixed = "The quick brown Fox; 42 jumps over the lazy dog!"
    assert apply(apply(mixed)) == mixed
