"""Tests for ipv6fmt: strict IPv6 expansion and RFC 5952 compression."""

import ast
import ipaddress
import random
from pathlib import Path

import pytest

from ipv6fmt import compress_ipv6, expand_ipv6

MODULE_PATH = Path(__file__).resolve().parent.parent / "ipv6fmt.py"

# --- Acceptance examples: expand -------------------------------------------

EXPAND_CASES = [
    ("::1", "0000:0000:0000:0000:0000:0000:0000:0001"),
    ("2001:db8::", "2001:0db8:0000:0000:0000:0000:0000:0000"),
    ("FF01:0:0:0:0:0:0:101", "ff01:0000:0000:0000:0000:0000:0000:0101"),
]


@pytest.mark.parametrize("addr,expected", EXPAND_CASES)
def test_expand_acceptance_examples(addr, expected):
    assert expand_ipv6(addr) == expected


# --- Acceptance examples: compress -----------------------------------------

COMPRESS_CASES = [
    ("2001:0db8:0000:0000:0000:ff00:0042:8329", "2001:db8::ff00:42:8329"),
    ("0000:0000:0000:0000:0000:0000:0000:0000", "::"),
    ("0000:0000:0000:0000:0000:0000:0000:0001", "::1"),
    ("ff01:0000:0000:0000:0000:0000:0000:0101", "ff01::101"),
    ("2001:0db8:0000:0001:0001:0001:0001:0001", "2001:db8:0:1:1:1:1:1"),
    ("1:0:0:2:0:0:0:3", "1:0:0:2::3"),
]


@pytest.mark.parametrize("addr,expected", COMPRESS_CASES)
def test_compress_acceptance_examples(addr, expected):
    assert compress_ipv6(addr) == expected


def test_single_zero_group_not_compressed():
    assert compress_ipv6("2001:0db8:0000:0001:0001:0001:0001:0001") == (
        "2001:db8:0:1:1:1:1:1"
    )


def test_equal_length_zero_runs_take_leftmost():
    # Two runs of length 2: at indices 0-1 and 3-4 and 6-7 -> leftmost wins.
    assert compress_ipv6("0:0:1:0:0:2:0:0") == "::1:0:0:2:0:0"
    assert compress_ipv6("1:0:0:2:0:0:0:3") == "1:0:0:2::3"


# --- Both functions accept expanded and compressed forms alike --------------

@pytest.mark.parametrize("addr,compressed", COMPRESS_CASES)
def test_expand_agrees_on_both_forms(addr, compressed):
    assert expand_ipv6(addr) == expand_ipv6(compressed)


@pytest.mark.parametrize("addr,compressed", COMPRESS_CASES)
def test_compress_idempotent_on_forms(addr, compressed):
    assert compress_ipv6(addr) == compressed
    assert compress_ipv6(compressed) == compressed
    assert compress_ipv6(expand_ipv6(addr)) == compressed


# --- Invalid addresses: ValueError for BOTH functions ------------------------

INVALID_ADDRESSES = [
    "",
    "1::2::3",
    "12345::",
    "gggg::",
    "1:2:3:4:5:6:7",
    "1:2:3:4:5:6:7:8:9",
    "1:2:3:4:5:6:7:8:9:a",
    ":1::2",
    "1::2:",
    ":",
    "1:2:3:4:5:6:7:8::",
    "::ffff:1.2.3.4",
    "fe80::1%eth0",
]


@pytest.mark.parametrize("addr", INVALID_ADDRESSES)
def test_expand_invalid_address_raises_value_error(addr):
    with pytest.raises(ValueError):
        expand_ipv6(addr)


@pytest.mark.parametrize("addr", INVALID_ADDRESSES)
def test_compress_invalid_address_raises_value_error(addr):
    with pytest.raises(ValueError):
        compress_ipv6(addr)


# --- Non-str input: TypeError for BOTH functions ----------------------------

def test_expand_non_str_raises_type_error():
    with pytest.raises(TypeError):
        expand_ipv6(123)


def test_compress_non_str_raises_type_error():
    with pytest.raises(TypeError):
        compress_ipv6(None)


# --- Property checks against stdlib ipaddress -------------------------------

def _random_address(rng):
    """Random 128-bit address; half of them forced to contain zero runs."""
    if rng.random() < 0.5:
        value = 0
        for i in range(8):
            group = rng.getrandbits(16)
            value = (value << 16) | group
        # Force a zero run so compression paths are exercised.
        start = rng.randrange(0, 6)
        length = rng.randint(1, 8 - start)
        for k in range(start, start + length):
            shift = 16 * (7 - k)
            value &= ~(0xFFFF << shift)
        return ipaddress.IPv6Address(value)
    return ipaddress.IPv6Address(rng.getrandbits(128))


def test_property_against_stdlib_ipaddress():
    rng = random.Random(20260558)
    for _ in range(200):
        ref = _random_address(rng)
        expanded = str(ref.exploded)
        compressed = str(ref.compressed)
        assert expand_ipv6(expanded) == ref.exploded
        assert expand_ipv6(compressed) == ref.exploded
        assert compress_ipv6(expanded) == ref.compressed
        assert compress_ipv6(compressed) == ref.compressed
        # compress is idempotent
        assert compress_ipv6(compress_ipv6(expanded)) == ref.compressed
        # expand(compressed form) == expand(expanded form)
        assert expand_ipv6(compressed) == expand_ipv6(expanded)


def test_property_tie_case_matches_stdlib():
    # Equal-length zero runs: leftmost must win, matching ipaddress.
    addr = "0:0:1:0:0:2:0:0"
    ref = ipaddress.IPv6Address(addr)
    assert compress_ipv6(addr) == ref.compressed
    assert compress_ipv6(addr) == "::1:0:0:2:0:0"


# --- Module isolation: stdlib only, no cross-imports ------------------------

def test_module_uses_only_stdlib_no_cross_imports():
    tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            imported.add(node.module.split(".")[0])
    assert imported <= {"re"}, "unexpected imports: %s" % sorted(imported)
    forbidden = {"ipaddr", "ipv4", "ipv4kit", "inversions", "egyptian"}
    assert not imported & forbidden
