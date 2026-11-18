"""tests/test_soundex.py: soundex 验收要点逐条测试（第四十一轮）。"""

import pytest

from soundex import soundex


def test_robert():
    assert soundex("Robert") == "R163"


def test_rupert():
    assert soundex("Rupert") == "R163"


def test_ashcraft():
    assert soundex("Ashcraft") == "A261"


def test_ashcroft():
    assert soundex("Ashcroft") == "A261"


def test_tymczak():
    assert soundex("Tymczak") == "T522"


def test_pfister():
    assert soundex("Pfister") == "P236"


def test_jackson():
    assert soundex("Jackson") == "J250"


def test_euler():
    assert soundex("Euler") == "E460"


def test_gauss():
    assert soundex("Gauss") == "G200"


def test_hilbert():
    assert soundex("Hilbert") == "H416"


def test_knuth():
    assert soundex("Knuth") == "K530"


def test_lee():
    assert soundex("Lee") == "L000"


def test_honeyman():
    assert soundex("Honeyman") == "H555"


def test_rubin():
    assert soundex("Rubin") == "R150"


def test_single_letter_a():
    assert soundex("A") == "A000"


def test_bb():
    assert soundex("BB") == "B000"


def test_babb():
    assert soundex("Babb") == "B100"


def test_robert_lowercase():
    assert soundex("robert") == "R163"


def test_empty_raises():
    with pytest.raises(ValueError):
        soundex("")


def test_non_alpha_raises():
    with pytest.raises(ValueError):
        soundex("A1")


def test_apostrophe_raises():
    with pytest.raises(ValueError):
        soundex("O'Brien")
