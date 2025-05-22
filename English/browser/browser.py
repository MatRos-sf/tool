__all__ = ["open_browser_with_vocabularies"]
import webbrowser
from typing import List

from English.vocabulary import Vocabulary

OXFORD_URL = "https://www.oxfordlearnersdictionaries.com/definition/english/{}?q={}"
DIKI_URL = "https://www.diki.pl/slownik-angielskiego?q={}"
GOOGLE_TRANSLATE_URL = "https://translate.google.com/?hl=en&sl=pl&tl=pl&text={}&op=translate"

def open_browser_with_vocabularies(list_of_vocabularies: List[Vocabulary]) -> None:
    """
    Opens a new browser window and tabs for each vocabulary entry. Tabs will be opened in the following order:
        1. Oxford dictionary
        2. Diki
        3. Google Translate with sentence
    """
    webbrowser.open_new("")
    for vocabulary in list_of_vocabularies:
        webbrowser.open_new_tab(OXFORD_URL.format(vocabulary.english, vocabulary.english))
        webbrowser.open_new_tab(DIKI_URL.format(vocabulary.english))
        webbrowser.open_new_tab(GOOGLE_TRANSLATE_URL.format(vocabulary.sentence.replace(" ", "%20")))
