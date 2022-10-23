# -*- coding: utf8 -*-
import pytest
from encoding import Soundex


@pytest.fixture
def soundex():
    return Soundex()


@pytest.mark.soundex_encoding
def test_pads_withzeros_to_ensure_three_digits(soundex):
    encoded = soundex.encode("I")
    assert encoded == "I000"


@pytest.mark.soundex_encoding
def test_retains_sole_letter_of_one_letter_word(soundex):
    encoded = soundex.encode("A")
    assert encoded == "A000"


@pytest.mark.soundex_encoding
def test_replaces_consonants_with_appropriate_digits(soundex):
    errors = []
    encoded = soundex.encode("Ab")
    if encoded != "A100":
        errors.append(f"Ab:\n-A100\n+{encoded}")

    encoded = soundex.encode("Ac")
    if encoded != "A200":
        errors.append(f"Ac:\n-A200\n+{encoded}")

    encoded = soundex.encode("Ad")
    if encoded != "A300":
        errors.append(f"Ad:\n-A300\n+{encoded}")

    encoded = soundex.encode("Ax")
    if encoded != "A200":
        errors.append(f"Ax:\n-A200\n+{encoded}")

    encoded = soundex.encode("A#")
    if encoded != "A000":
        errors.append(f"A#:\n-A000\n+{encoded}")

    joined_errors = "\n".join(errors)
    assert not errors, f"errors occured:\n{joined_errors}"

@pytest.mark.soundex_encoding
def test_empty_word_returns_empty(soundex):
    encoded = soundex.encode("")
    assert encoded == ""

@pytest.mark.soundex_encoding
def test_replaces_multiple_consonants_with_digits(soundex):
    encoded = soundex.encode("Acdl")
    assert encoded == "A234"

@pytest.mark.soundex_encoding
def test_limits_length_to_4_characters(soundex):
    encoded = soundex.encode("Dcdlbefgt")
    assert encoded == "D234"

@pytest.mark.soundex_encoding
def test_ignores_vowels_like_letters(soundex):
    encoded = soundex.encode("BaAeiouhHyYcdl")
    assert encoded == "B234"

@pytest.mark.soundex_encoding
def test_combine_duplicate_encodings(soundex):
    assert Soundex.encoded_digit("b") == Soundex.encoded_digit("f")
    assert Soundex.encoded_digit("c") == Soundex.encoded_digit("g")
    assert Soundex.encoded_digit("d") == Soundex.encoded_digit("t")
    encoded = soundex.encode("Abfcgdt")
    assert encoded == "A123"

@pytest.mark.soundex_encoding
def test_uppercases_first_letter(soundex):
    encoded = soundex.encode("abcd")
    assert encoded[0] == "A"

@pytest.mark.soundex_encoding
def test_ignores_case_when_encoding_consonants(soundex):
    assert soundex.encode("BCDL") == soundex.encode("Bcdl")

@pytest.mark.soundex_encoding
def test_combines_duplicate_codes_when_2nd_letter_duplicates_1st(soundex):
    assert soundex.encode("Bbcd") == "B230"
