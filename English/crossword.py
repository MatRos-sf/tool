"""
This module contains functions that import raw vocabulary from a file, and prepare it
for the crossword puzzle https://crosswordlabs.com/ website.

"""
from dataclasses import dataclass
from pathlib import Path
from random import shuffle

IMPORT_VOCABULARIES_PATH = Path(__file__).parent.parent / "files" / "english" / "raw_vocabularies"
PAYLOAD_TO_CROSSWORD_PATH = Path(__file__).parent.parent / "files" / "english" / "payload_to_crossword"

LIST_OF_VOCABULARIES = []
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
        data = [x.strip() for x in data]
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

if __name__ == "__main__":
    print("Importing vocabularies")
    import_voc_from_file_to_list()
    print("Shuffling vocabularies")
    shuffle(LIST_OF_VOCABULARIES)
    print("Saving vocabularies")
    save_voc_to_file()
    print("Vocabularies have been saved")
