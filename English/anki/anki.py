import csv
from typing import List
from pathlib import Path
from datetime import datetime

from English.vocabulary import Vocabulary
from English.anki.field import Extend

def create_anki_csv(path: Path, list_of_vocabularies: List[Vocabulary]):
    with open(path, "w", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")
        for voc in list_of_vocabularies:
            row = []
            for field in Extend:
                if hasattr(voc, field):
                    row.append(getattr(voc, field))
                if field == Extend.TAG:
                    row.append(datetime.strftime(datetime.now(), "%b").lower())
                else:
                    row.append("")
            writer.writerow(row)
