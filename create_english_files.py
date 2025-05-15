from pathlib import Path
from random import shuffle
import argparse
from typing import List
import os

from English.vocabulary import import_voc_from_file_to_list
from English.crossword import save_voc_to_file
from English.choice_section import choose_choice_words, save_choice_words
from English.anki.anki import create_anki_csv



def command_separated_list(value) -> List[int]:
    try:
        return [int(x) for x in value.split(",")]
    except ValueError:
        raise argparse.ArgumentTypeError("List of integers expected")

parser = argparse.ArgumentParser(description="Script to create English files for: crossword, choices and anki")

parser.add_argument(
    "--path_raw",
    type=str,
    default=os.getcwd(),
    # required=True,
    help="Path to raw vocabularies",
)

parser.add_argument(
    "--tag",
    type=command_separated_list,
    help='Comma-separated list of integers where 1 = crossword, 2 = choices, 3 = anki',
    default=[1, 2, 3]
)

args = parser.parse_args()
print("Importing vocabularies")
list_of_vocabularies = import_voc_from_file_to_list(Path(args.path_raw) / Path("raw_vocabularies"))
print("Shuffling vocabularies")
shuffle(list_of_vocabularies)

for tag in args.tag:
    if tag == 1:
        filepath = Path(args.path_raw) / "crossword.txt"
        print("Saving vocabularies to crossword")
        save_voc_to_file(filepath, list_of_vocabularies)
        print("Vocabularies have been saved in the path: ", filepath)
    if tag == 2:
        filepath = Path(args.path_raw) / "choices.txt"
        print("Creating choices")
        choices = choose_choice_words(list_of_vocabularies)
        print("Saving choices")
        save_choice_words(choices, filepath)
        print("Choices have been saved to the path: ", filepath)
    if tag == 3:
        filepath = Path(args.path_raw) / Path("anki.csv")
        print("Creating anki csv")
        create_anki_csv(filepath, list_of_vocabularies)
        print("Anki csv has been created in the path: ", filepath.resolve())
