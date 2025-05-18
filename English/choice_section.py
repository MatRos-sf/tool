"""
This module provides utility functions for generating vocabulary revision choices.
Example use case: generating randomized vocabulary exercises for practice.
"""

from enum import IntEnum
from typing import List
from random import shuffle, randint
from string import ascii_lowercase, ascii_uppercase
from pathlib import Path

from .vocabulary import Vocabulary

class SuffixEnum(IntEnum):
    ALPHABET_LOWER = 1
    NUMBER = 2
    ALPHABET_UPPER = 3

def shuffle_words_by_labels(list_of_voc: List[Vocabulary], labels: List[str]):
    """
    Shuffles the list of vocabulary objects and creates a new list of lists of mixed words.
    """
    mixed = []
    for label in labels:
        helper_list = [getattr(attr, label) for attr in list_of_voc]
        shuffle(helper_list)
        mixed.append(helper_list)
    return mixed

def generate_suffix(suffix: SuffixEnum, position: int):
    match suffix:
        case SuffixEnum.ALPHABET_LOWER:
            return ascii_lowercase[position]
        case SuffixEnum.NUMBER:
            return str(position)
        case SuffixEnum.ALPHABET_UPPER:
            return ascii_uppercase[position]
        case _:
            raise NotImplementedError(f"Case not implemented {suffix}")

def choose_choice_words(list_of_voc: List["Vocabulary"])-> List[List[str]]:
    rand = randint(1,2)
    match rand:
        case 1:
            return shuffle_words_by_labels(list_of_voc, ["english", "definition", "polish"])
        case 2:
            return shuffle_words_by_labels(list_of_voc, ["english", "sentence_with_gap"])
        case _:
            raise NotImplementedError(f"Case not implemented {rand}")


def save_choice_words(list_of_choices: List[List[str]], path_name: Path| str ):
    with open(path_name, "w", encoding="utf-8") as file:
        for words, suffix_type in zip(list_of_choices, SuffixEnum):
            for idx, word in enumerate(words):
                payload = generate_suffix(suffix_type, idx) + ". " + word
                file.write(payload + "\n")
            file.write("\n" + '*'*50 + "\n")