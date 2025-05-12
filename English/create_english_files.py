from pathlib import Path
from random import shuffle

from English.vocabulary import import_voc_from_file_to_list
from English.crossword import save_voc_to_file
from English.choice_section import chose_choice_words, save_choice_words

DIR_BASE_SAVE = Path(__file__).parent.parent / "files" / "english"
IMPORT_VOCABULARIES_PATH = DIR_BASE_SAVE / "raw_vocabularies"
PAYLOAD_TO_CROSSWORD_PATH = DIR_BASE_SAVE/ "payload_to_crossword"
CHOICES_PATH = DIR_BASE_SAVE / "choices"

if __name__ == "__main__":
    print("Importing vocabularies")
    list_of_vocabularies = import_voc_from_file_to_list(IMPORT_VOCABULARIES_PATH)
    print("Shuffling vocabularies")
    shuffle(list_of_vocabularies)
    print("Saving vocabularies")
    save_voc_to_file(PAYLOAD_TO_CROSSWORD_PATH, list_of_vocabularies)
    print("Vocabularies have been saved")
    print("Creating choices")
    choices = chose_choice_words(list_of_vocabularies)
    print("Saving choices")
    save_choice_words(choices, CHOICES_PATH)
    print("Choices have been saved")