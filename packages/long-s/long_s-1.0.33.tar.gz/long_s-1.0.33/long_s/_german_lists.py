"""
Filename: _german_lists.py
Description: This file contains functionality 
             to load German spelling patterns from .json files.
            
             The best way to modify these lists is to activate developer mode
             before any conversions are run:
                long_s.enable_developer_mode()

             Upon loading dictionaries, this will automatically clean up 
             the .json files under ./german-lists/raw and then generate new
             .json files under ./german-lists/processed.


Author: TravisGK
Version: 1.0.6


The final patterns are organized and indexed as such:
    EXACT_MATCHES:
        alphabetized -> src

    LONG_S_NAMES:
        alphabetized -> src

    FORCED_OVERWRITES: 
        -> src

    END_PATTERNS: 
        end indexes -> src

    OMNIPRESENT_PATTERNS:
        indexed by letters all contained -> min(MAX_S_COUNT, num of S) -> src

    START_PATTERNS: 
        alphabetized -> src

    POSTPROCESS_PATTERNS: 
        -> src


License: MIT License
"""

import json
import os
from ._simple_conversions import strip_consonant_accents


def _get_local_file_dir():
    file_path = os.path.abspath(__file__)
    return os.path.dirname(file_path)


def using_developer_mode():
    return _USING_DEV_MODE


_USING_DEV_MODE = False


def enable_developer_mode():
    """
    Turns the option on to automatically clean up
    and reprocess the .json files full of spelling patterns.
    """
    global _USING_DEV_MODE
    _USING_DEV_MODE = True


_CUSTOM_ALPHABET = "0123456789'-aäbcdefghijklmnoöpqrsſßtuüvwxyz"
_index_map = {char: index for index, char in enumerate(_CUSTOM_ALPHABET)}


def sort_words(words, length_as_primary=True):
    """
    Returns the given list of words sorted
    by descending length and then alphabetically.

    Parameters:
    words (list): list of words to be sorted.
    length_as_primary (bool): if False,
                              then the list will be sorted alphabetically.
    """
    if length_as_primary:
        return sorted(
            words,
            key=lambda word: (-len(word), [_index_map[char.lower()] for char in word]),
        )
    return sorted(words, key=lambda word: [_index_map[char.lower()] for char in word])


def _load_json(json_path: str):
    """Loads a list/dictionary object from the given file path."""
    with open(json_path, "r", encoding="utf-8") as file:
        result = json.load(file)

    return result


def _load_json_as_alphabet_indexed(json_path: str, sort_lists: bool = True):
    """
    Loads the list from the given <json_path> and sorts
    each list item into a sublist, with each sublist being
    indexed by the first letter of the list item.

    Parameters:
    json_path (str): the .json file that will be loaded.

    Returns:
    dict: each key is a letter in the alphabet and its corresponding value
          will be the list of items, with the list being sorted.
    """
    ALPHABET = "aäbcdefghijklmnoöpqrstuüvwxyz"
    result = {}

    loaded_list = _load_json(json_path)
    for word in loaded_list:
        index = word[0]
        if index == "ſ":
            index = "s"
        if index in ALPHABET:
            if result.get(index) is None:
                result[index] = []
            result[index].append(word)

    if sort_lists:
        keys_list = sort_words(result.keys())
        for key in keys_list:
            result[key] = sort_words(result[key])

    return result


def _load_json_as_indexed_by_end(keys, json_path: str, sort_lists: bool = True):
    """
    Returns a dictionary with the contents of a .json file broken
    into sublists that are indexed by the ending letters.

    Parameters:
    keys (list): the ending sequences to sort by.
    json_path (str): the path to the .json file to load from.
    """
    loaded_list = _load_json(json_path)

    result = {key: [] for key in keys}

    for key in keys:
        remaining_list = []
        for word in loaded_list:
            clean_word = word.replace("ſ", "s")
            if clean_word.endswith(key):
                result[key].append(word)
            else:
                remaining_list.append(word)
        loaded_list = remaining_list
        if sort_lists:
            result[key] = sort_words(result[key])

    return result


def _count_s(word: str):
    """Returns the number of times S occurs in the string."""
    word = word.lower()
    short_count = word.count("s")
    long_count = word.count("ſ")
    return short_count + long_count


def _load_json_as_indexed_by_contained(
    keys, json_path: str, max_s_count: int = 2, sort_lists: bool = True
):
    """
    Loads a .json file as a dictionary and processes it
    so its words to be indexed by contained letters.
    """
    # result = {key: {i for i in range(1, max_s_count + 1)} for key in keys}
    loaded_list = _load_json(json_path)

    result = {}

    # organizes all the patterns by the letters they contain.
    for key in keys:
        remaining_list = []
        for word in loaded_list:
            if all(c in word for c in key):
                subdict = result.get(key)
                if subdict is None:
                    result[key] = {}

                s_count = min(max_s_count, _count_s(word))
                subdict = result[key].get(s_count)
                if subdict is None:
                    result[key][s_count] = []
                result[key][s_count].append(word)
            else:
                remaining_list.append(word)

        loaded_list = remaining_list

    # puts the remainders under their own key.
    result["remaining"] = {}
    if len(loaded_list) > 0:
        for word in loaded_list:
            s_count = min(max_s_count, _count_s(word))
            subdict = result["remaining"].get(s_count)
            if subdict is None:
                result["remaining"][s_count] = []
            result["remaining"][s_count].append(word)

    # sorts everything and then returns the result.
    if sort_lists:
        for key in keys + ["remaining"]:
            for i in range(1, max_s_count + 1):
                result[key][i] = sort_words(result[key][i])

    return result


def _get_flattened_terms(terms, results_list):
    """
    Returns a 1D list of all words contained
    in the multidimensional dictionary of <terms>.
    """
    if isinstance(terms, list):
        results_list.extend(terms)
        return

    if isinstance(terms, dict):
        for key in terms.values():
            _get_flattened_terms(key, results_list)
    else:
        for term in terms:
            results_list.extend(_get_flattened_terms(term, results_list))


def save_flattened_json(terms, json_path: str):
    """
    Saves a multidimensional list/dictionary as a 1D list to a .json file.
    This keeps the lists easy to edit for future patches.
    """
    flat_list = []
    _get_flattened_terms(terms, flat_list)
    flat_list = list(set(flat_list))
    flat_list = sort_words(flat_list, length_as_primary=False)
    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(flat_list, file, indent=4, ensure_ascii=False)


def _save_json(terms, json_path: str):
    """Saves a list/dictionary object to the given file path."""
    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(terms, file, indent=4, ensure_ascii=False)


_DICTS = [
    {},  # 0 exact-matches
    {},  # 1 long-s-names
    [],  # 2 forced-overwrites
    {},  # 3 end-patterns
    {},  # 4 omnipresent-patterns
    {},  # 5 start-patterns
    [],  # 6 postprocess-patterns
]


def get_german_dicts():
    load_dicts()
    return _DICTS


END_KEYS = [
    "ens",
    "ers",
    "gem",
    "gen",
    "ger",
    "ges",
    "nem",
    "nen",
    "ner",
    "rem",
    "ren",
    "rer",
    "res",
    "sem",
    "sen",
    "tem",
    "ten",
    "ter",
    "tes",
    "em",
    "en",
    "es",
    "ge",
    "ms",
    "ne",
    "ns",
    "re",
    "se",
    "te",
    "ts",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "k",
    "l",
    "m",
    "n",
    "p",
    "r",
    "s",
    "t",
    "v",
    "z",
]

CONTAINING_KEYS = [
    "ir",
    "nt",
    "er",
    "et",
    "en",
    "at",
    "r",
    "ea",
    "e",
    "n",
    "i",
    "a",
    "t",
    "h",
    "u",
    "o",
]

_processed_file_paths = []
_loaded = False


def get_processed_file_paths():
    load_dicts()
    return _processed_file_paths


def load_dicts(sort_lists=True):
    """Loads all the spelling patterns to memory if not yet done."""
    global _loaded
    if _loaded:
        return

    global _processed_file_paths
    global _DICTS
    ENFORCE_PROCESSING = _USING_DEV_MODE
    CLEAN_UP_RAW_FILES = _USING_DEV_MODE

    # .json files whose contents are already a direct 1D list.
    DIRECT_FILE_NAMES = [
        "2-forced-overwrites.json",
        "6-postprocess-patterns.json",
    ]

    # .json files whose contents are
    # indexed alphabetically by their first letter.
    ALPHABETIC_FILE_NAMES = [
        "1-exact-matches.json",
        "1-long-s-names.json",
        "5-start-patterns.json",
    ]

    END_PATTERN_FILE_NAME = "3-end-patterns.json"
    OMNIPRESENT_FILE_NAME = "4-omnipresent-patterns.json"

    # ensures that the needed text resources are present.
    local_dir = _get_local_file_dir()
    raw_path = os.path.join(local_dir, "german-lists", "raw")
    if not os.path.isdir(raw_path):
        print(f"There was no German resource directory found at {raw_path}.")
        return

    # determines if the lists need to be processed and saved.
    must_process = True
    processed_path = os.path.join(local_dir, "german-lists", "processed")
    _processed_file_paths = [
        os.path.join(processed_path, ALPHABETIC_FILE_NAMES[0]),
        os.path.join(processed_path, ALPHABETIC_FILE_NAMES[1]),
        os.path.join(processed_path, DIRECT_FILE_NAMES[0]),
        os.path.join(processed_path, END_PATTERN_FILE_NAME),
        os.path.join(processed_path, OMNIPRESENT_FILE_NAME),
        os.path.join(processed_path, ALPHABETIC_FILE_NAMES[2]),
        os.path.join(processed_path, DIRECT_FILE_NAMES[1]),
    ]
    if not os.path.isdir(processed_path):
        os.path.mkdir(processed_path)
    elif not ENFORCE_PROCESSING and all(
        os.path.isfile(f) for f in _processed_file_paths
    ):
        must_process = False

    # loads the dictionaries from the already-existing processed files.
    if not must_process:
        for i, file_path in enumerate(_processed_file_paths):
            _DICTS[i] = _load_json(file_path)
        return

    # processes files that are already 1D lists.
    for file_name in DIRECT_FILE_NAMES:
        in_file_path = os.path.join(raw_path, file_name)
        out_file_path = os.path.join(processed_path, file_name)
        direct_list = _load_json(in_file_path)
        if sort_lists:
            direct_list = sort_words(direct_list)
        _save_json(direct_list, out_file_path)

    # processes files to be indexed by their starting letter.
    for file_name in ALPHABETIC_FILE_NAMES:
        in_file_path = os.path.join(raw_path, file_name)
        out_file_path = os.path.join(processed_path, file_name)
        dict_obj = _load_json_as_alphabet_indexed(in_file_path)
        _save_json(dict_obj, out_file_path)

    # processes the file with end patterns.
    in_file_path = os.path.join(raw_path, END_PATTERN_FILE_NAME)
    out_file_path = os.path.join(processed_path, END_PATTERN_FILE_NAME)
    dict_obj = _load_json_as_indexed_by_end(END_KEYS, in_file_path)
    _save_json(dict_obj, out_file_path)

    # processes the file with omnipresent patterns.
    in_file_path = os.path.join(raw_path, OMNIPRESENT_FILE_NAME)
    out_file_path = os.path.join(processed_path, OMNIPRESENT_FILE_NAME)
    dict_obj = _load_json_as_indexed_by_contained(CONTAINING_KEYS, in_file_path)
    _save_json(dict_obj, out_file_path)

    # loads the processed files so py-long-s can run.
    for i, file_path in enumerate(_processed_file_paths):
        _DICTS[i] = _load_json(file_path)

    # sorts and overwrites the raw files.
    if CLEAN_UP_RAW_FILES:
        raw_file_paths = [
            os.path.join(raw_path, ALPHABETIC_FILE_NAMES[0]),
            os.path.join(raw_path, ALPHABETIC_FILE_NAMES[1]),
            os.path.join(raw_path, DIRECT_FILE_NAMES[0]),
            os.path.join(raw_path, END_PATTERN_FILE_NAME),
            os.path.join(raw_path, OMNIPRESENT_FILE_NAME),
            os.path.join(raw_path, ALPHABETIC_FILE_NAMES[2]),
            os.path.join(raw_path, DIRECT_FILE_NAMES[1]),
        ]
        for i, out_file_path in enumerate(raw_file_paths):
            save_flattened_json(_DICTS[i], out_file_path)

    _loaded = True
