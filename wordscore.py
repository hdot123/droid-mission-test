"""wordscore: compute a word's letter-position score.

Spec (work order): score(word) sums each letter's alphabetical position
(a=1 ... z=26, case-insensitive), ignoring non-letter characters.
An empty string, or a string with no letters, returns 0.

Worked examples from the deliverable section (verbatim):
    score("abc") returns 6
    score("z") returns 26
    score("a-b") returns 3

The acceptance section additionally requires score("bad") to equal 7 and
score("abc") to equal 7. That pair is carried verbatim in
tests/test_wordscore.py and is deliberately not reconciled here: this module
implements only the position-sum formula stated in the spec.

Standard library only; no imports of caesar/hexcolor; no CLI.
"""


def score(word):
    """Return the sum of alphabetical positions of the letters in word.

    Letters score by alphabetical position (a=1 ... z=26), case-insensitively.
    Non-letter characters are ignored. An empty string, or a string without
    letters, returns 0.

    Deliverable examples: score("abc") returns 6, score("z") returns 26,
    score("a-b") returns 3.
    """
    total = 0
    for ch in word:
        if "a" <= ch <= "z":
            total += ord(ch) - ord("a") + 1
        elif "A" <= ch <= "Z":
            total += ord(ch) - ord("A") + 1
    return total
