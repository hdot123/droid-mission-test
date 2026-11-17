"""wordscore: score a word by the alphabetical positions of its letters.

Spec (work order, verbatim rules):
- iterate over the characters of the word;
- take each letter's alphabetical position (a=1 ... z=26, case-insensitive);
- ignore all non-letter characters;
- return the sum of the positions;
- an empty string or a string with no letters returns 0.

Standard library only. No CLI, no package directory, no imports from other
modules.
"""


def score(word):
    """Return the sum of alphabetical positions of the letters in word.

    Non-letter characters are ignored; an empty string or a string with no
    letters returns 0.

    Examples given in the work order (preserved verbatim, including the
    contradictory ones -- see tests/test_wordscore.py):
        score("abc") -> 6   (deliverable example)
        score("z")   -> 26  (deliverable example)
        score("a-b") -> 3   (deliverable example)
        score("bad") -> 7   (acceptance-criteria example)
        score("abc") -> 7   (acceptance-criteria example)
    """
    total = 0
    for ch in word:
        low = ch.lower()
        if "a" <= low <= "z":
            total += ord(low) - ord("a") + 1
    return total
