"""
Filename: _simpler_conversions.py
Description: This contains the simpler functions that insert the long S
			 into these languages: English, French, Spanish, and Italian.

Author: TravisGK
Version: 1.0

License: MIT License
"""

import re
from unidecode import unidecode


def strip_accents(word: str):
    """Returns the given text with any accent marks removed."""
    PLACEHOLDER = "\t"
    word = word.replace("ß", PLACEHOLDER)
    clean_word = unidecode(word)
    clean_word = clean_word.replace(PLACEHOLDER, "ß")
    return clean_word


def strip_consonant_accents(word: str):
    """Returns text with any accent marks over only consonants removed."""
    result = ""
    no_accents = strip_accents(word)
    for i, n_char in enumerate(no_accents):
        if n_char in "AEIOUYaeiouy":
            result += word[i]
        else:
            result += n_char

    return result


def strip_to_german_alphabet(word: str):
    """
    Returns text with any accent marks removed (besides umlauts).
    If there's an issue due to a foreign character
    (i.e. one character becomes two),
    then the word is just returned.
    """
    result = ""
    no_accents = strip_accents(word)
    if len(word) != len(no_accents):
        return word

    for i, n_char in enumerate(no_accents):
        # print(f"{word}\t{no_accents}\t{i} len word: {len(word)}")
        if word[i] in "AÄEIOÖUÜYaäeioöuüy":
            result += word[i]
        else:
            result += n_char

    return result


def apply_long_S_pattern(word: str, pattern: str):
    """
    Returns the result of using the given re pattern
    to select occurrences of the letter S and replace them with a long S.
    None will be returned if no replacments are made.
    """
    indices = [m.start() for m in re.finditer(pattern, word)]

    if len(indices) == 0:
        return None  # there are no replacements to be made.

    # makes replacements at the identified locations.
    for index in indices:
        word = word[:index] + "ſ" + word[index + 1 :]

    return word


def transfer_long_S(processed_word: str, original_word: str):
    """
    This function is given the processed word with any long S (ſ),
    which will generally lack accents and capitalization,
    and transfer any long S to the given original word,
    so that the capitalization and accents of the original text
    are ultimately maintained.

    Parameters:
    processed_word (string): text that's already had the long S (ſ) inserted.
    original_word (string): text whose capitalization and accents
                            are to be preserved.

    Returns:
    string: the processed_word with the decor of the original_word.
    """

    if len(processed_word) != len(original_word):
        return processed_word

    for i, p_char in enumerate(processed_word):
        o_char = original_word[i]
        if o_char == "s":
            original_word = original_word[:i] + p_char + original_word[i + 1 :]

    return original_word


def convert_english_word(word: str):
    """Returns English text with the long S (ſ) placed appropriately."""
    no_accents = strip_accents(word.lower())

    # looks for any "S" that's followed by a line break (but not a hyphen)
    # or a letter other than
    # F, B (old books only), K (old books only),
    # and is also NOT preceded by the letter F.
    SHORT_BEFORE_B_AND_K = False  # historical variation.

    if SHORT_BEFORE_B_AND_K:
        pattern = r"(?<!f)s(?=[ac-eg-jl-z—])"
    else:
        pattern = r"(?<!f)s(?=[a-eg-z—])"

    no_accents = apply_long_S_pattern(no_accents, pattern)
    if no_accents is None:
        return word  # there are no replacements to be made.

    no_accents = no_accents.replace("ſſſ", "ſsſ")

    word = transfer_long_S(no_accents, word)

    return word


def convert_french_word(word: str):
    """Returns French text with the long S (ſ) placed appropriately."""
    no_accents = strip_accents(word.lower())

    # looks for any "S" that's followed by a letter other than B, F, or H.
    no_accents = apply_long_S_pattern(no_accents, r"s(?=[ac-egi-z])")
    if no_accents is None:
        return word  # there are no replacements to be made.

    word = transfer_long_S(no_accents, word)

    return word


def convert_spanish_word(word: str):
    """Returns Spanish text with the long S (ſ) placed appropriately."""

    clean_word = strip_consonant_accents(word.lower())

    # looks for any "S" that's followed by a letter other than B, F, H,
    # or an accented vowel. it can also be followed by a hyphen or line-break.
    clean_word = apply_long_S_pattern(clean_word, r"s(?=[ac-egi-z-—])")
    if clean_word is None:
        return word  # there are no replacements to be made.

    clean_word = clean_word.replace("ſſi", "ſsi")

    word = transfer_long_S(clean_word, word)
    return word


def convert_italian_word(word: str):
    """Returns Italian text with the long S (ſ) placed appropriately."""

    MAINTAIN_DOUBLE_LONG_WITH_SSI = True  # historical variation.
    clean_word = strip_consonant_accents(word.lower())

    # looks for any "S" that's followed by a letter other than B, F,
    # or an accented vowel.
    clean_word = apply_long_S_pattern(clean_word, r"s(?=[ac-eg-z-—])")
    if clean_word is None:
        return word  # there are no replacements to be made.

    if not MAINTAIN_DOUBLE_LONG_WITH_SSI:
        clean_word = clean_word.replace("ſſi", "ſsi")

    word = transfer_long_S(clean_word, word)
    return word
