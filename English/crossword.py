"""
This module contains functions that import raw vocabulary from a file, and prepare it
for the crossword puzzle https://crosswordlabs.com/ website.

"""
from dataclasses import dataclass
from pathlib import Path
from random import shuffle, randint
from typing import List
from enum import IntEnum
from string import ascii_lowercase, ascii_uppercase

DIR_BASE_SAVE = Path(__file__).parent.parent / "files" / "english"
IMPORT_VOCABULARIES_PATH = DIR_BASE_SAVE / "raw_vocabularies"
PAYLOAD_TO_CROSSWORD_PATH = DIR_BASE_SAVE/ "payload_to_crossword"
CHOICES_PATH = DIR_BASE_SAVE / "choices"

LIST_OF_VOCABULARIES = []

class SuffixEnum(IntEnum):
    ALPHABET_LOWER = 1
    NUMBER = 2
    ALPHABET_UPPER = 3

@dataclass
class Vocabulary:
    english: str
    phonetic: str
    part_of_speach: str
    definition: str
    polish: str
    sentence: str
    sentence_with_gap: str

    def prepare_payload_to_crossword(self):
        """
        Prepares a string payload that will be written to the file that will be used
        to generate a crossword puzzle.

        The format of the string is:
        <English_word> (<Part_of_speech>) <Definition> | <Sentence_with_gap>

        :return: str
        """
        english = self.english.replace(" ", "_")
        return "{} ({}) {} | {}".format(english, self.part_of_speach, self.definition, self.sentence_with_gap)

    @classmethod
    def parse(cls, data: list):
        assert all(isinstance(x, str) for x in data)
        # remove emtpy space
        data = [x.strip().replace("*", "") for x in data]
        return cls(*data)

def import_voc_from_file_to_list():
    """
    Imports raw vocabulary from file and creates list of Vocabulary objects
    """
    with open(IMPORT_VOCABULARIES_PATH, "r", encoding="utf-8") as file:
        raw = file.read()
    raw = raw.replace("\n", ";").split("|")[1:-1]
    raw = list(filter(lambda x: x != ';', raw))
    assert len(raw) % 7 == 0, "The table should have 7 columns"
    start = 0
    for end in range(0, len(raw), 7):
        LIST_OF_VOCABULARIES.append(Vocabulary.parse(raw[start:end+7]))
        start = end + 7

def save_voc_to_file(path: Path = PAYLOAD_TO_CROSSWORD_PATH):
    """
    Saves the list of Vocabulary objects to a file.

    Args:
        path (Path): The file path where the vocabularies will be saved.
                     Defaults to PAYLOAD_TO_CROSSWORD_PATH.
    """
    with open(path, "w", encoding="utf-8") as file:
        # Iterate over each vocabulary object in the list
        for voc in LIST_OF_VOCABULARIES:
            # Write the prepared payload for each vocabulary to the file
            file.write(voc.prepare_payload_to_crossword() + "\n")

def choice_words(list_of_voc: List[Vocabulary], labels: List[str]):
    """
    Shuffles the list of vocabulary objects and creates a new list of lists of mixed words.
    """
    mixed = []
    for label in labels:
        helper_list = [getattr(attr, label) for attr in list_of_voc]
        shuffle(helper_list)
        mixed.append(helper_list)
    return mixed

def save_choice_words(list_of_choices: List[List[str]], path_name: Path| str = CHOICES_PATH):
    with open(path_name, "w", encoding="utf-8") as file:
        for idx_suffix, words in enumerate(list_of_choices):
            for idx, word in enumerate(words):
                payload = set_suffix(SuffixEnum(idx_suffix+1), idx) + ". " + word
                file.write(payload + "\n")
            file.write("\n" + '*'*50 + "\n")

def set_suffix(suffix: SuffixEnum, position: int):
    match suffix:
        case SuffixEnum.ALPHABET_LOWER:
            return ascii_lowercase[position]
        case SuffixEnum.NUMBER:
            return str(position)
        case SuffixEnum.ALPHABET_UPPER:
            return ascii_uppercase[position]
        case _:
            raise NotImplementedError(f"Case not implemented {suffix}")

def chose_choice_words(list_of_voc: List[Vocabulary])-> List[List[str]]:
    rand = randint(1,2)
    match rand:
        case 1:
            return choice_words(list_of_voc, ["english", "definition", "polish"])
        case 2:
            return choice_words(list_of_voc, ["english", "sentence_with_gap"])
        case _:
            raise NotImplementedError(f"Case not implemented {rand}")

if __name__ == "__main__":
    print("Importing vocabularies")
    import_voc_from_file_to_list()
    print("Shuffling vocabularies")
    shuffle(LIST_OF_VOCABULARIES)
    print("Saving vocabularies")
    save_voc_to_file()
    print("Vocabularies have been saved")
    print("Creating choices")
    choices = chose_choice_words(LIST_OF_VOCABULARIES)
    print("Saving choices")
    save_choice_words(choices)
    print("Choices have been saved")
