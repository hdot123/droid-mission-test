"""Tests for the hexcolor module only (#RGB / #RRGGBB parse and to_hex)."""

import pytest

import hexcolor


class TestParse:
    def test_rrggbb_spec_example(self):
        assert hexcolor.parse("#FF8000") == (255, 128, 0)

    def test_rgb_shorthand_spec_example(self):
        assert hexcolor.parse("#f80") == (255, 136, 0)

    def test_mixed_case_spec_example(self):
        assert hexcolor.parse("#0a1B2c") == (10, 27, 44)

    def test_black(self):
        assert hexcolor.parse("#000000") == (0, 0, 0)

    def test_white(self):
        assert hexcolor.parse("#FFFFFF") == (255, 255, 255)

    def test_shorthand_uppercase(self):
        assert hexcolor.parse("#F8A") == (255, 136, 170)

    def test_returns_int_tuple(self):
        result = hexcolor.parse("#010203")
        assert isinstance(result, tuple)
        assert all(isinstance(v, int) for v in result)
        assert result == (1, 2, 3)

    @pytest.mark.parametrize("bad", ["FF8000", "f80", "", "ff8000"])
    def test_missing_hash(self, bad):
        with pytest.raises(ValueError):
            hexcolor.parse(bad)

    @pytest.mark.parametrize(
        "bad",
        ["#", "#F", "#FF", "#FFFF", "#FFFFF", "#FFFFFFF"],
    )
    def test_bad_length(self, bad):
        with pytest.raises(ValueError):
            hexcolor.parse(bad)

    @pytest.mark.parametrize(
        "bad",
        ["#GGGGGG", "#ff800g", "#f8x", "#12 456", "#ff800 ", "#zzz"],
    )
    def test_non_hex_characters(self, bad):
        with pytest.raises(ValueError):
            hexcolor.parse(bad)


class TestToHex:
    def test_spec_example(self):
        assert hexcolor.to_hex(255, 128, 0) == "#ff8000"

    def test_black_spec_example(self):
        assert hexcolor.to_hex(0, 0, 0) == "#000000"

    def test_lowercase_output(self):
        assert hexcolor.to_hex(10, 27, 44) == "#0a1b2c"

    def test_bounds(self):
        assert hexcolor.to_hex(0, 255, 255) == "#00ffff"
        assert hexcolor.to_hex(255, 0, 1) == "#ff0001"

    @pytest.mark.parametrize(
        "args",
        [(256, 0, 0), (0, 256, 0), (0, 0, 256), (300, 300, 300)],
    )
    def test_component_above_range(self, args):
        with pytest.raises(ValueError):
            hexcolor.to_hex(*args)

    @pytest.mark.parametrize(
        "args",
        [(-1, 0, 0), (0, -1, 0), (0, 0, -1)],
    )
    def test_component_below_range(self, args):
        with pytest.raises(ValueError):
            hexcolor.to_hex(*args)

    @pytest.mark.parametrize(
        "args",
        [("1", 0, 0), (0, 12.5, 0), (0, 0, None), ("255", "0", "0")],
    )
    def test_non_integer_component(self, args):
        with pytest.raises(ValueError):
            hexcolor.to_hex(*args)


class TestRoundTrip:
    @pytest.mark.parametrize(
        "color, expected",
        [
            ("#ff8000", "#ff8000"),
            ("#f80", "#ff8800"),
            ("#0a1b2c", "#0a1b2c"),
            ("#010203", "#010203"),
            ("#ffffff", "#ffffff"),
            ("#000000", "#000000"),
        ],
    )
    def test_parse_to_hex_round_trip(self, color, expected):
        # Shorthand expands, so "#f80" round-trips to "#ff8000".
        assert hexcolor.to_hex(*hexcolor.parse(color)) == expected
