import pytest

from English.browser.oxford_tool import (
    capture_phonetic_from_oxford,
    check_phonetic,
    create_oxford_url,
)
from English.vocabulary import Vocabulary

from .conftest import HTML_WITHOUT_DIV, HTML_WITHOUT_SPAN, SUCCESS_HTML


@pytest.mark.parametrize(
    "key, expected",
    [
        (
            "poverty",
            "https://www.oxfordlearnersdictionaries.com/definition/english/poverty?q=poverty",
        ),
        (
            "dog",
            "https://www.oxfordlearnersdictionaries.com/definition/english/dog?q=dog",
        ),
        (
            "corn dog",
            "https://www.oxfordlearnersdictionaries.com/definition/english/corn-dog?q=corn+dog",
        ),
        ("", "https://www.oxfordlearnersdictionaries.com/definition/english/?q="),
    ],
)
def test_create_query_string_for_oxford(key, expected):
    assert create_oxford_url(key) == expected


# @patch("httpx.AsyncClient.get", return_value=httpx.Response(status_code=200, text=MOCK_HTML))
@pytest.mark.asyncio
async def test_capture_phonetic_from_oxford(mock_oxford_response):
    word = Vocabulary("", "", "", "", "", "", "")
    mock_oxford_response(200, SUCCESS_HTML)
    result = await capture_phonetic_from_oxford(word)
    assert result == "/dɒɡ/"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status_code, text", [(200, HTML_WITHOUT_DIV), (200, HTML_WITHOUT_SPAN), (404, "")]
)
async def test_capture_phonetic_from_oxford_error(
    mock_oxford_response, status_code, text
):
    word = Vocabulary("", "", "", "", "", "", "")
    mock_oxford_response(status_code, text)
    with pytest.raises(Exception):
        await capture_phonetic_from_oxford(word)


@pytest.mark.asyncio
async def test_check_phonetic(mock_gen_oxford_response, vocabulary_dog, vocabulary_cat):
    # activate mock
    next(mock_gen_oxford_response())
    words = [vocabulary_dog, vocabulary_cat]
    result = await check_phonetic(words)
    assert len(result) == 1
    assert result[0][0] == vocabulary_dog.phonetic
    assert result[0][1] == "/dɒɡ/"
