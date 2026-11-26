"""Title-style capitalization.

``title_case`` converts arbitrary text to title case with the exact rules
pinned by the round-55 acceptance spec:

* whitespace runs collapse to single spaces; leading/trailing stripped;
* each word: first alphabetic char uppercased, remaining letters lowercased,
  leading symbols preserved as-is;
* small words (a, an, the, ...) stay lowercase only when the word is neither
  first nor last;
* hyphenated compounds are handled segment by segment: first segment always
  capitalized, later segments lowercase when they are small words;
* abbreviations are not preserved as all-caps (NASA -> Nasa);
* non-str input raises TypeError.
"""

SMALL_WORDS = frozenset(
    {
        "a",
        "an",
        "the",
        "and",
        "but",
        "or",
        "nor",
        "for",
        "so",
        "yet",
        "at",
        "by",
        "in",
        "into",
        "of",
        "off",
        "on",
        "onto",
        "per",
        "to",
        "up",
        "via",
        "as",
    }
)


def _letters(word):
    return "".join(ch for ch in word if ch.isalpha())


def _capitalize(word):
    """Uppercase the first letter, lowercase all other letters.

    Non-letter characters (leading symbols, digits, apostrophes) are kept
    as-is. A word with no letters at all is returned unchanged.
    """
    out = []
    seen_letter = False
    for ch in word:
        if not ch.isalpha():
            out.append(ch)
        elif not seen_letter:
            out.append(ch.upper())
            seen_letter = True
        else:
            out.append(ch.lower())
    return "".join(out)


def _lowercase(word):
    return "".join(ch.lower() if ch.isalpha() else ch for ch in word)


def _format_segment(segment, force_capitalize=False):
    if force_capitalize:
        return _capitalize(segment)
    if _letters(segment).lower() in SMALL_WORDS:
        return _lowercase(segment)
    return _capitalize(segment)


def title_case(text: str) -> str:
    """Return ``text`` in title case according to the pinned rules."""
    if not isinstance(text, str):
        raise TypeError(
            "title_case() expected str, got %s" % type(text).__name__
        )
    words = text.split()
    if not words:
        return ""
    last = len(words) - 1
    formatted = []
    for index, word in enumerate(words):
        segments = word.split("-")
        out_segments = []
        for seg_index, segment in enumerate(segments):
            if len(segments) == 1:
                # Plain word: small words lowercase only when neither first
                # nor last; first or last word is capitalized like normal.
                if index == 0 or index == last:
                    out_segments.append(_capitalize(segment))
                else:
                    out_segments.append(_format_segment(segment))
            elif seg_index == 0:
                # Hyphenated compound: first segment always capitalized.
                out_segments.append(_capitalize(segment))
            else:
                # Later segments: still lowercase if they are small words.
                out_segments.append(_format_segment(segment))
        formatted.append("-".join(out_segments))
    return " ".join(formatted)


if __name__ == "__main__":
    import sys

    for arg in sys.argv[1:]:
        print(title_case(arg))
