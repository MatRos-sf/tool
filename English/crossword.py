"""
This module contains functions that import raw vocabulary from a file, and prepare it
for the crossword puzzle https://crosswordlabs.com/ website.

"""
from pathlib import Path
from typing import List

from English.vocabulary import Vocabulary

def save_voc_to_file(path: Path, list_of_voc: List[Vocabulary]):
    """
    Saves the list of Vocabulary objects to a file.

    Args:
        path (Path): The file path where the vocabularies will be saved.
                     Defaults to PAYLOAD_TO_CROSSWORD_PATH.
        list_of_voc (List[Vocabulary]): A list of Vocabulary objects to be saved.
    """
    with open(path, "w", encoding="utf-8") as file:
        # Iterate over each vocabulary object in the list
        for voc in list_of_voc:
            # Write the prepared payload for each vocabulary to the file
            file.write(voc.prepare_payload_to_crossword() + "\n")

