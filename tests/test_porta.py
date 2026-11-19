import pytest

from porta import porta_decrypt, porta_encrypt


# --- basic single-letter keys --------------------------------------------

def test_encrypt_hello_key_a():
    assert porta_encrypt("HELLO", "A") == "URYYB"


def test_encrypt_hello_key_b():
    assert porta_encrypt("HELLO", "B") == "URYYB"


def test_encrypt_hello_key_c():
    assert porta_encrypt("HELLO", "C") == "VSZZA"


def test_encrypt_hello_key_z():
    assert porta_encrypt("HELLO", "Z") == "TQXXC"


def test_encrypt_full_alphabet_key_m():
    assert (
        porta_encrypt("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "M")
        == "TUVWXYZNOPQRSHIJKLMABCDEFG"
    )


# --- multi-letter keys ----------------------------------------------------

def test_encrypt_attackatdawn_lemon():
    assert porta_encrypt("ATTACKATDAWN", "LEMON") == "SEAUVPPAXTEL"


def test_encrypt_thequickbrownfox_zebra():
    assert porta_encrypt("THEQUICKBROWNFOX", "ZEBRA") == "HWRIHURXWECHANBL"


def test_encrypt_hello_world_key():
    assert porta_encrypt("HELLO WORLD", "KEY") == "ZTXQM KJCXV"


# --- decryption -----------------------------------------------------------

def test_decrypt_seauppaxtel_lemon():
    assert porta_decrypt("SEAUVPPAXTEL", "LEMON") == "ATTACKATDAWN"


@pytest.mark.parametrize(
    "text, key",
    [
        ("MEETMEATNOON", "SECRET"),
        ("BALLOON", "ZEBRA"),
        ("THE RAIN IN SPAIN", "MONARCHY"),
    ],
)
def test_roundtrip(text, key):
    assert porta_decrypt(porta_encrypt(text, key), key) == text


# --- edge cases -----------------------------------------------------------

def test_empty_text():
    assert porta_encrypt("", "KEY") == ""


def test_non_letters_preserved():
    assert porta_encrypt("ABC123", "A") == "NOP123"


def test_lowercase_key_accepted():
    assert porta_encrypt("HELLO", "a") == "URYYB"


# --- validation -----------------------------------------------------------

@pytest.mark.parametrize("key", ["", "K3Y"])
def test_bad_key_raises_value_error(key):
    with pytest.raises(ValueError):
        porta_encrypt("HELLO", key)


@pytest.mark.parametrize("text, key", [(123, "KEY"), ("HELLO", 5)])
def test_bad_types_raise_type_error(text, key):
    with pytest.raises(TypeError):
        porta_encrypt(text, key)


def test_decrypt_bad_key_raises_value_error():
    with pytest.raises(ValueError):
        porta_decrypt("HELLO", "")


def test_decrypt_bad_types_raise_type_error():
    with pytest.raises(TypeError):
        porta_decrypt(None, "KEY")
    with pytest.raises(TypeError):
        porta_decrypt("HELLO", None)
