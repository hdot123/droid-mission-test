"""tests for pluralize."""
import pytest

from pluralize import pluralize


def test_cat():
    assert pluralize("cat") == "cats"


def test_dog():
    assert pluralize("dog") == "dogs"


def test_city():
    assert pluralize("city") == "cities"


def test_baby():
    assert pluralize("baby") == "babies"


def test_day():
    assert pluralize("day") == "days"


def test_boy():
    assert pluralize("boy") == "boys"


def test_box():
    assert pluralize("box") == "boxes"


def test_class():
    assert pluralize("class") == "classes"


def test_watch():
    assert pluralize("watch") == "watches"


def test_wish():
    assert pluralize("wish") == "wishes"


def test_child():
    assert pluralize("child") == "children"


def test_person():
    assert pluralize("person") == "people"


def test_mouse():
    assert pluralize("mouse") == "mice"


def test_sheep():
    assert pluralize("sheep") == "sheep"


def test_fish():
    assert pluralize("fish") == "fish"


def test_leaf():
    assert pluralize("leaf") == "leaves"


def test_knife():
    assert pluralize("knife") == "knives"


def test_life():
    assert pluralize("life") == "lives"


def test_wolf():
    assert pluralize("wolf") == "wolves"


def test_roof():
    assert pluralize("roof") == "roofs"


def test_hero():
    assert pluralize("hero") == "heroes"


def test_potato():
    assert pluralize("potato") == "potatoes"


def test_photo():
    assert pluralize("photo") == "photos"


def test_piano():
    assert pluralize("piano") == "pianos"


def test_echo():
    assert pluralize("echo") == "echoes"


def test_quiz():
    assert pluralize("quiz") == "quizzes"


def test_church():
    assert pluralize("church") == "churches"


def test_bus():
    assert pluralize("bus") == "buses"


def test_toy():
    assert pluralize("toy") == "toys"


def test_key():
    assert pluralize("key") == "keys"


def test_empty_raises():
    with pytest.raises(ValueError):
        pluralize("")


def test_uppercase_raises():
    with pytest.raises(ValueError):
        pluralize("Cat")


def test_non_ascii_raises():
    with pytest.raises(ValueError):
        pluralize("cat!")


def test_none_raises_type():
    with pytest.raises(TypeError):
        pluralize(None)


def test_int_raises_type():
    with pytest.raises(TypeError):
        pluralize(3)
