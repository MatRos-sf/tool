import argparse
import os
import warnings
from pathlib import Path
from random import shuffle
from typing import List

from English.anki import ANKI_FIELDS, create_anki_csv
from English.browser import open_browser_with_vocabularies
from English.choice_section import choose_choice_words, save_choice_words
from English.crossword import save_voc_to_file
from English.vocabulary import import_voc_from_file_to_list


def command_separated_list(value) -> List[int]:
    try:
        return [int(x) for x in value.split(",")]
    except ValueError:
        raise argparse.ArgumentTypeError("List of integers expected")


parser = argparse.ArgumentParser(
    description="Script to create English files for: crossword, choices and anki"
)

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
    help="Comma-separated list of integers where 1 = crossword, 2 = choices, 3 = anki",
    default=[1, 2, 3],
)
parser.add_argument(
    "--type_anki_field",
    help="Type of anki field. Anki field are implemented in anki/filed directory with ANKI_FIELD variables."
    "If you want create new one please implemented it in ANKI_FIELD dictionary. ",
    default="extend",
)

parser.add_argument(
    "--mix",
    type=bool,
    default=False,
    help="If true, vocabularies will be shuffled before processing",
)

args = parser.parse_args()
print("Importing vocabularies")
list_of_vocabularies = import_voc_from_file_to_list(
    Path(args.path_raw) / Path("raw_vocabularies")
)

if args.mix:
    print("Shuffling vocabularies")
    shuffle(list_of_vocabularies)

# GUARD
if args.type_anki_field != "extend":
    if 3 not in args.tag:
        warnings.warn(
            "You can't use --type_anki_field without --tag 3, so --type_anki_field will be ignored"
        )
    elif not ANKI_FIELDS.get(args.type_anki_field.title()):
        raise ValueError(
            f"Type of anki field {args.type_anki_field} is not implemented. You can only use: {', '.join(ANKI_FIELDS.keys())}"
        )

field = ANKI_FIELDS[args.type_anki_field.lower()]

output_path = {
    1: Path(args.path_raw) / "crossword.txt",
    2: Path(args.path_raw) / "choices.txt",
    3: Path(args.path_raw) / "anki.csv",
}

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
        create_anki_csv(filepath, list_of_vocabularies, field)
        print("Anki csv has been created in the path: ", filepath.resolve())

    if tag == 4:
        print("Opening browser")
        open_browser_with_vocabularies(list_of_vocabularies)
        print("Browser has been opened")
