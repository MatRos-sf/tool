import re
from dataclasses import dataclass
from pathlib import Path

IMPORT_VOCABULARIES_PATH = Path(__file__).parent.parent / "files" / "english" / "raw_vocabularies"

@dataclass
class Vocabulary:
    english: str
    phonetic: str
    part_of_speach: str
    definition: str
    polish: str
    sentence: str

with open(IMPORT_VOCABULARIES_PATH, "r", encoding="utf-8") as file:
    raw = file.read()

raw = raw.replace("\n", ";").split("|")[1:-1]
raw = list(filter(lambda x: x != ';', raw))
print(len(raw))
print(raw)