from http import HTTPStatus

import requests
from bs4 import BeautifulSoup

from English.vocabulary import Vocabulary

OXFORD_URL = "https://www.oxfordlearnersdictionaries.com/definition/english/{}?q={}"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
}


def create_query_string_for_oxford(key: str, *, deep: bool = False, number: int = 1):
    return OXFORD_URL.format(key.replace(" ", "-"), key.replace(" ", "+"))


def capture_phonetic_from_oxford(word: Vocabulary) -> str:
    url = create_query_string_for_oxford(word.english)
    request = requests.get(url, headers=HEADERS, timeout=10)

    if request.status_code == HTTPStatus.OK:
        soup = BeautifulSoup(request.text, "html.parser")
        phonetic_uk_section = soup.find_all("div", {"class": "phons_br"})

        if phonetic_uk_section:
            phonetic_uk_section = phonetic_uk_section[0]
            for child in phonetic_uk_section.children:
                if child.name == "span":
                    return child.text.strip()

    raise Exception(f"Cannot find phonetic for word: {word.english}")


def check_phonetic(words: list[Vocabulary]):
    phonetic_difference = []
    for word in words:
        try:
            phonetic_from_oxford = capture_phonetic_from_oxford(word)
        except Exception:
            print(f"Cannot find phonetic for word: {word.english}")
            continue
        if word.phonetic != phonetic_from_oxford:
            phonetic_difference.append((word.phonetic, phonetic_from_oxford))

    return phonetic_difference
