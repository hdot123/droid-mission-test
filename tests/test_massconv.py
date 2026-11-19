import pytest

from massconv import mass_convert

TOL = 1e-9


def test_kg_to_g():
    assert mass_convert(1, "kg", "g") == 1000.0


def test_g_to_mg():
    assert mass_convert(1, "g", "mg") == pytest.approx(1000.0, abs=TOL)


def test_t_to_kg():
    assert mass_convert(1, "t", "kg") == 1000.0


def test_mg_to_g():
    assert mass_convert(1000, "mg", "g") == pytest.approx(1.0, abs=TOL)


def test_lb_to_kg():
    assert mass_convert(1, "lb", "kg") == pytest.approx(0.45359237, abs=TOL)


def test_oz_to_lb():
    assert mass_convert(16, "oz", "lb") == pytest.approx(1.0, abs=TOL)


def test_oz_to_g():
    assert mass_convert(1, "oz", "g") == pytest.approx(28.349523125, abs=TOL)


def test_st_to_lb():
    assert mass_convert(1, "st", "lb") == 14.0


def test_st_to_kg():
    assert mass_convert(1, "st", "kg") == pytest.approx(6.35029318, abs=TOL)


def test_zero_value():
    assert mass_convert(0, "t", "lb") == 0.0


def test_kg_to_lb():
    assert mass_convert(2.5, "kg", "lb") == pytest.approx(5.511556554621939, abs=TOL)


def test_roundtrip_lb_kg():
    assert mass_convert(mass_convert(3.7, "lb", "kg"), "kg", "lb") == pytest.approx(3.7, abs=TOL)


def test_roundtrip_st_g():
    assert mass_convert(mass_convert(2, "st", "g"), "g", "st") == pytest.approx(2.0, abs=TOL)


def test_same_unit():
    assert mass_convert(42, "kg", "kg") == 42.0


def test_unknown_to_unit():
    with pytest.raises(ValueError):
        mass_convert(1, "kg", "slug")


def test_unknown_from_unit():
    with pytest.raises(ValueError):
        mass_convert(1, "slug", "kg")


def test_non_numeric_value():
    with pytest.raises(TypeError):
        mass_convert("1", "kg", "g")


def test_bool_value_rejected():
    with pytest.raises(TypeError):
        mass_convert(True, "kg", "g")
