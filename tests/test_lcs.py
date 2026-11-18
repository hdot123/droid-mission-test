from lcs import lcs_length, lcs_string


def test_length_spec_example():
    assert lcs_length("ABCBDAB", "BDCABA") == 4


def test_string_spec_example():
    assert lcs_string("ABCBDAB", "BDCABA") == "BCBA"


def test_string_second_spec_example():
    assert lcs_string("AGGTAB", "GXTXAYB") == "GTAB"


def test_no_common_subsequence_length():
    assert lcs_length("abc", "def") == 0


def test_no_common_subsequence_string():
    assert lcs_string("abc", "def") == ""


def test_empty_first_string():
    assert lcs_string("", "abc") == ""
    assert lcs_length("", "abc") == 0


def test_empty_second_string():
    assert lcs_string("abc", "") == ""
    assert lcs_length("abc", "") == 0


def test_both_empty():
    assert lcs_length("", "") == 0
    assert lcs_string("", "") == ""


def test_subsequence_of_one_string():
    assert lcs_string("abcde", "ace") == "ace"
    assert lcs_length("abcde", "ace") == 3


def test_identical_strings():
    assert lcs_length("aaaa", "aaaa") == 4
    assert lcs_string("aaaa", "aaaa") == "aaaa"


def test_tie_break_prefers_skipping_a():
    # Both sides tie at the first step; the pinned rule skips a's current
    # character, which keeps b's characters and yields "a" (the opposite
    # tie-break would yield "b").
    assert lcs_string("ab", "ba") == "a"
    # Another tie point: must follow the pinned rule, not the other side.
    assert lcs_string("ABCBDAB", "BDCABA") == "BCBA"


def test_result_is_common_subsequence():
    a, b = "ABCBDAB", "BDCABA"
    result = lcs_string(a, b)
    assert len(result) == lcs_length(a, b)
    it = iter(a)
    assert all(ch in it for ch in result)


def test_length_matches_string_length():
    pairs = [
        ("ABCBDAB", "BDCABA"),
        ("AGGTAB", "GXTXAYB"),
        ("abcde", "ace"),
        ("abc", "def"),
        ("", "abc"),
        ("", ""),
        ("AAAA", "AA"),
    ]
    for a, b in pairs:
        assert lcs_length(a, b) == len(lcs_string(a, b))
