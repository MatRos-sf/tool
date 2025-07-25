from dataclasses import dataclass
from pathlib import Path
from typing import List, Union


@dataclass
class Vocabulary:
    english: str
    phonetic: str
    part_of_speech: str
    definition: str
    polish: str
    sentence: str
    sentence_with_gap: str

    def prepare_payload_to_crossword(self) -> str:
        """
        Prepares a string payload that will be written to the file that will be used
        to generate a crossword puzzle.

        The format of the string is:
        <English_word> (<Part_of_speech>) <Definition> | <Sentence_with_gap>

        :return: str
        """
        english = self.english.replace(" ", "_")
        return "{} ({}) {} | {}".format(
            english, self.part_of_speech, self.definition, self.sentence_with_gap
        )

    @classmethod
    def parse(cls, data: list) -> "Vocabulary":
        assert all(isinstance(x, str) for x in data)
        # remove emtpy space
        data = [x.strip().replace("*", "") for x in data]
        return cls(*data)

    def backup_payload(self) -> str:
        return "| {} | {} | {} | {} | {} | {} | {} |".format(
            self.english,
            self.phonetic,
            self.part_of_speech,
            self.definition,
            self.polish,
            self.sentence,
            self.sentence_with_gap,
        )

    def __str__(self):
        return f"{self.english} → {self.polish}"


def import_voc_from_file_to_list(path: Union[str, Path]) -> List[Vocabulary]:
    """
    Imports raw vocabulary from file and creates list of Vocabulary objects
    """
    list_of_vocabularies = []
    with open(path, "r", encoding="utf-8") as file:
        raw = file.read()
    raw = raw.replace("\n", ";").split("|")[1:-1]
    raw = list(filter(lambda x: x != ";", raw))
    assert len(raw) % 7 == 0, "The table should have 7 columns"
    for i in range(0, len(raw), 7):
        # First and Second column scip
        if i in (0, 7):
            continue
        list_of_vocabularies.append(Vocabulary.parse(raw[i : i + 7]))
    return list_of_vocabularies
