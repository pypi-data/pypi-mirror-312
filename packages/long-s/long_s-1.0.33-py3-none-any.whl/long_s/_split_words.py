"""
Filename: _split_words.py
Description: This file contains a function that will take a sentence
             and return a list of each contained individual word
             along with its objective index in the sentence.
             This goes beyond splitting, since this ensures
             there's no surrounding punctuation in the result.

Author: TravisGK
Version: 1.0

License: MIT License
"""

import re
import unicodedata


def _is_letter(char: str):
    """Returns True if the given <char> is some letter."""
    category = unicodedata.category(char)
    return category.startswith("L")


def split_words_with_indices(text: str, lang: str):
    """
    This function takes the given text and splits it into a list of words,
    with each word having its index in the original text provided.
    the function also considers language-specific rules for word splitting.

    Parameters:
    text (string): the string to be split.
    lang (string): the language code (to handle specific rules).

    Returns:
    list of tuples: each tuple contains the word itself
                    and its start index in the original text.
    """

    APOSTROPHES = "'"

    # finds the contents and the index of every word.
    matches = re.finditer(r"\S+", text)
    results = []
    for match in matches:
        word = match.group()
        global_index = match.start()

        # the "word" could contain punctuation,
        # so the program runs along until it hits a letter,
        # which will be the local starting index.
        local_start_offset = 0
        for i in range(len(word)):
            if _is_letter(word[i]):
                # a letter was found, so this is where the word begins.
                local_start_offset = i
                break
        else:
            # no letter was ever found,
            # so this group of text is not a word
            # and should be skipped.
            continue

        # now the local ending index is found.
        local_end_offset = len(word) - 1
        is_german = lang == "de"
        for i in range(len(word) - 1, -1, -1):
            if _is_letter(word[i]) or (is_german and word[i] in APOSTROPHES):
                # this is where the word ends.
                local_end_offset = i
                break

        # with the local starting and ending index,
        # the objective tuple can be created.
        word = word[local_start_offset : local_end_offset + 1]
        index = global_index + local_start_offset
        results.append((word, index))

    return results
