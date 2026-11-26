"""tests for unaccent.strip_accents —— 逐字覆盖规格验收要点。"""

import unicodedata

import pytest

from unaccent import strip_accents


def test_basic_accents():
    assert strip_accents("café") == "cafe"
    assert strip_accents("naïve") == "naive"
    assert strip_accents("Zürich") == "Zurich"
    assert strip_accents("résumé") == "resume"
    assert strip_accents("Ångström") == "Angstrom"
    assert strip_accents("niño") == "nino"
    assert strip_accents("čau") == "cau"
    assert strip_accents("őrség") == "orseg"
    assert strip_accents("tiếng Việt") == "tieng Viet"
    assert strip_accents("İstanbul") == "Istanbul"


def test_no_decomposition_mapping_letters_preserved():
    # 规格明示：无分解映射的字母原样保留，不是遗漏。
    assert strip_accents("Æsop") == "Æsop"
    assert strip_accents("smørrebrød") == "smørrebrød"


def test_plain_and_edge_inputs():
    assert strip_accents("plain ascii") == "plain ascii"
    assert strip_accents("") == ""
    assert strip_accents("東京") == "東京"


def test_decomposed_spelling_e_acute():
    # e + 组合尖音符的分解拼写
    assert strip_accents("é") == "e"


def test_both_spellings_of_A_ring_agree():
    # 预合成拼写与分解拼写同果
    assert strip_accents("Å") == "A"
    assert strip_accents("Å") == "A"


def test_more_phrases():
    assert strip_accents("crème brûlée") == "creme brulee"
    assert strip_accents("façade") == "facade"
    assert strip_accents("señor") == "senor"


def test_output_contains_no_mn_characters():
    samples = [
        "café",
        "Ångström",
        "tiếng Việt",
        "İstanbul",
        "őrség",
        "crème brûlée",
        "é",
        "Å",
        "smørrebrød",
        "Æsop",
    ]
    for s in samples:
        out = strip_accents(s)
        assert all(unicodedata.category(ch) != "Mn" for ch in out), out


def test_idempotent():
    samples = ["café", "Ångström", "tiếng Việt", "őrség", "é", "Å", ""]
    for s in samples:
        once = strip_accents(s)
        assert strip_accents(once) == once


def test_nfd_and_nfc_input_spellings_agree():
    pairs = [
        ("café", unicodedata.normalize("NFD", "café")),
        ("Ångström", unicodedata.normalize("NFD", "Ångström")),
        ("tiếng Việt", unicodedata.normalize("NFD", "tiếng Việt")),
        ("é", unicodedata.normalize("NFD", "é")),
        ("Å", unicodedata.normalize("NFD", "Å")),
    ]
    for nfc, nfd in pairs:
        assert strip_accents(nfc) == strip_accents(nfd)


def test_type_error_non_str():
    with pytest.raises(TypeError):
        strip_accents(123)
    with pytest.raises(TypeError):
        strip_accents(None)
