"""Score verdict helper: pass at 70 or above, fail otherwise."""


def verdict(score):
    """Return "pass" if score >= 70, else "fail"."""
    if score >= 70:
        return "pass"
    return "fail"
