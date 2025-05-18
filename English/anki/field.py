__all__ = ["ANKI_FIELDS", "AnkiField"]
from enum import StrEnum
from typing import Protocol
from datetime import datetime

class AnkiField(Protocol):
    @classmethod
    def create_anki(cls, list_of_vocabularies: list):
        ...


class Extend(StrEnum):
    ENGLISH = "english"
    AUDIO_ENGLISH = "audio_english"
    PHONETIC = "phonetic"
    PART_OF_SPEECH = "part_of_speech"
    DEFINITION = "definition"
    POLISH = "polish"
    SENTENCE = "sentence"
    AUDIO_SENTENCE = "audio_sentence"
    SENTENCE_WITH_GAP = "sentence_with_gap"
    DEF_TIP = "def-tip"
    TAG = "tag"

    @classmethod
    def row_generate(cls, list_of_vocabularies):
        for voc in list_of_vocabularies:
            row = []
            for field in cls:
                if hasattr(voc, field):
                    row.append(getattr(voc, field))
                elif field == Extend.TAG:
                    row.append(datetime.strftime(datetime.now(), "%b").lower())
                else:
                    row.append(" ")
            yield row

ANKI_FIELDS = {
    "extend": Extend
}