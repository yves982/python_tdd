# -*- coding: utf-8 -*-
from collections import OrderedDict

class Soundex:
    """
    The Soundex class.
    """

    MAX_CODE_LENGTH = 4
    WORDS = {
        "b": "1", "f": "1", "p": "1", "v": "1",
        "c": "2", "g": "2", "j": "2", "k": "2", "q": "2", "s": "2", "x": "2", "z": "2",
        "d": "3", "t": "3",
        "l": "4",
        "m": "5", "n": "5",
        "r": "6"
    }
    MAX_ENCODED_LENGTH = 4
    NOT_A_DIGIT = "*"

    def encode(self, word: str):
        head = Soundex.__head_with_first_letter_uppercased(word)
        encoded_word = Soundex.__encoded_digits(word)
        encoded = Soundex.__zero_pad(head + encoded_word)[0:Soundex.MAX_ENCODED_LENGTH]
        return encoded

    @staticmethod
    def encoded_digit(word: str):
        first_letter = word[0].lower()
        has_letter = first_letter in Soundex.WORDS
        return Soundex.WORDS[first_letter] if has_letter else Soundex.NOT_A_DIGIT

    @staticmethod
    def __encoded_digits(word: str):
        encoded_chars = [Soundex.encoded_digit(char) for char in word]
        encoded_chars = Soundex.__remove_adjacent_doubles(encoded_chars)
        encoded_chars = Soundex.__remove_first_if_same_encoding_as_head(encoded_chars, word)
        return "".join(encoded_chars).replace(Soundex.NOT_A_DIGIT, "")

    @staticmethod
    def __remove_first_if_same_encoding_as_head(encoded_chars, word):
        if len(encoded_chars) > 0 and encoded_chars[0] == Soundex.encoded_digit(word[0]):
            encoded_chars = encoded_chars[1:]
        return encoded_chars

    @staticmethod
    def __zero_pad(word: str):
        length = len(word)
        zeros_needed = Soundex.MAX_CODE_LENGTH - length if length > 0 else 0
        return word + zeros_needed * "0"

    @staticmethod
    def __head_with_first_letter_uppercased(word: str):
        return word[0].upper() if len(word) > 0 else ""

    @staticmethod
    def __tail(word: str):
        return word[1:] if len(word) > 1 else Soundex.NOT_A_DIGIT

    @staticmethod
    def __remove_adjacent_doubles(encoded_chars: list[str]):
        return [_char if _char != encoded_chars[index-1] else Soundex.NOT_A_DIGIT for index, _char
                in enumerate(encoded_chars)]
