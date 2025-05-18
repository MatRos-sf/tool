__all_ = ["create_anki_csv"]
import csv
from typing import List
from pathlib import Path

from English.vocabulary import Vocabulary
from .field import AnkiField

def create_anki_csv(path: Path, list_of_vocabularies: List[Vocabulary], cls_field: AnkiField):
    with open(path, "w", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")
        for row in cls_field.create_anki(list_of_vocabularies):
            writer.writerow(row)
