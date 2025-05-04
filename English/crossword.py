import re
from dataclasses import dataclass
from pathlib import Path

IMPORT_VOCABULARIES_PATH = Path(__file__).parent.parent / "files" / "english" / "raw_vocabularies"

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
    @classmethod
    def parse(cls, data: list):
        #TODO: clean white space,
        return cls(*data)

def create_voc():
    with open(IMPORT_VOCABULARIES_PATH, "r", encoding="utf-8") as file:
        raw = file.read()
    raw = raw.replace("\n", ";").split("|")[1:-1]
    raw = list(filter(lambda x: x != ';', raw))
    assert len(raw) % 7 == 0, "The table should have 7 columns"
    start = 0
    for end in range(7, len(raw), 7):
        LIST_OF_VOCABULARIES.append(Vocabulary(*raw[start:end]))
        start = end

