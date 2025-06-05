import asyncio
from http import HTTPStatus
from typing import List

import httpx
from bs4 import BeautifulSoup

from English.vocabulary import Vocabulary

OXFORD_URL = "https://www.oxfordlearnersdictionaries.com/definition/english/{}?q={}"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
}


def create_oxford_url(key: str):
    return OXFORD_URL.format(key.replace(" ", "-"), key.replace(" ", "+"))


async def capture_phonetic_from_oxford(word: Vocabulary) -> str:
    """
    Checks phonetic of word according to Oxford dictionary.

    Function parsing html and looking for span section with uk phonetic.
    Returns:
        str: Phonetic of word
    Raises:
        Exception: If phonetic is not found or status code is not 200
    """
    url = create_oxford_url(word.english)

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS, timeout=10)
    if response.status_code == HTTPStatus.OK:
        soup = BeautifulSoup(response.text, "html.parser")
        phonetic_uk_section = soup.find_all("div", {"class": "phons_br"})
        if phonetic_uk_section:
            phonetic_uk_section = phonetic_uk_section[0]
            for child in phonetic_uk_section.children:
                if child.name == "span":
                    return child.text.strip()

    raise Exception(f"Cannot find phonetic for word: {word.english}")


async def check_phonetic(words: list[Vocabulary]) -> List[tuple[str, str]]:
    """
    Checks phonetic of words according to Oxford dictionary and return difference between them.
    returns:
        List[tuple[str, str]]: List of phonetic differences where first element is current phonetic and second is phonetic from Oxford dictionary
    """
    phonetic_difference = []
    tasks = [capture_phonetic_from_oxford(word) for word in words]
    result = await asyncio.gather(*tasks, return_exceptions=True)
    for word, phonetic in zip(words, result):
        if word.phonetic != phonetic:
            phonetic_difference.append((word.phonetic, phonetic))
    return phonetic_difference
