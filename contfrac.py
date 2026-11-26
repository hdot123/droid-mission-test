"""Continued-fraction expansion and convergents for rational numbers.

Standard library only; this module does not import any other project module.
"""

from fractions import Fraction


def _require_int(value, name):
    """Raise TypeError unless value is a genuine int (bool excluded)."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be int, got {type(value).__name__}")


def to_contfrac(num: int, den: int) -> list[int]:
    """Expand the rational num/den into a continued fraction.

    Floor semantics: the first term may be negative, every later term is
    >= 1, and when the expansion has more than one term the last term is
    >= 2 (canonical form).  True floor division is used throughout, never
    truncating division, so e.g. -7/5 -> [-2, 1, 1, 2].
    """
    _require_int(num, "num")
    _require_int(den, "den")
    if den <= 0:
        raise ValueError(f"den must be > 0, got {den!r}")
    terms = []
    while True:
        a = num // den  # floor division, correct even for negative num
        terms.append(a)
        num -= a * den  # 0 <= remainder < den
        if num == 0:
            break
        num, den = den, num
    # Canonical form: a trailing 1 merges into the previous term ([..., a, 1]
    # == [..., a + 1]).  The Euclidean remainder sequence makes this
    # unreachable with floor semantics, but keep it canonical defensively.
    if len(terms) > 1 and terms[-1] == 1:
        terms.pop()
        terms[-1] += 1
    return terms


def from_contfrac(terms) -> Fraction:
    """Evaluate a continued-fraction expansion, returning a Fraction.

    The first term may be any int; every later term must be >= 1.
    """
    try:
        items = list(terms)
    except TypeError:
        raise TypeError(f"terms must be a sequence of int, got {type(terms).__name__}") from None
    if not items:
        raise ValueError("continued fraction must have at least one term")
    for i, t in enumerate(items):
        _require_int(t, f"term {i}")
    for i, t in enumerate(items[1:], start=1):
        if t < 1:
            raise ValueError(f"term {i} must be >= 1, got {t!r}")
    value = Fraction(items[-1])
    for t in reversed(items[:-1]):
        value = t + 1 / value
    return value


def convergents(num: int, den: int) -> list[Fraction]:
    """Return the successive convergents of num/den, in order.

    The last convergent equals the original fraction.
    """
    terms = to_contfrac(num, den)
    h_prev, h_prev2 = 1, 0  # h_{-1}, h_{-2}
    k_prev, k_prev2 = 0, 1  # k_{-1}, k_{-2}
    result = []
    for a in terms:
        h = a * h_prev + h_prev2
        k = a * k_prev + k_prev2
        result.append(Fraction(h, k))
        h_prev2, h_prev = h_prev, h
        k_prev2, k_prev = k_prev, k
    return result
