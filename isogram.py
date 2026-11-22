"""Isogram (non-repeating-letter) checks."""

from __future__ import annotations

__all__ = ["is_isogram", "repeated_letters"]


def _letters(word: str) -> list[str]:
    if not isinstance(word, str):
        raise TypeError(f"word must be str, got {type(word).__name__}")
    return [ch.lower() for ch in word if "a" <= ch.lower() <= "z"]


def is_isogram(word: str) -> bool:
    """Return True when no a-z letter repeats (case-insensitive, non-letters ignored)."""
    letters = _letters(word)
    return len(letters) == len(set(letters))


def repeated_letters(word: str) -> list[str]:
    """Return the letters occurring more than once, in alphabetical order."""
    counts: dict[str, int] = {}
    for ch in _letters(word):
        counts[ch] = counts.get(ch, 0) + 1
    return sorted(ch for ch, n in counts.items() if n > 1)
