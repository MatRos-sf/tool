from unittest.mock import patch

import httpx
import pytest

from English.vocabulary import Vocabulary

SUCCESS_HTML = """
<div class="phons_br" wd="dog" htag="div" geo="br" hclass="phons_br"><div class="sound audio_play_button pron-uk icon-audio" data-src-mp3="https://www.oxfordlearnersdictionaries.com/media/english/uk_pron/d/dog/dog__/dog__gb_2.mp3" data-src-ogg="https://www.oxfordlearnersdictionaries.com/media/english/uk_pron_ogg/d/dog/dog__/dog__gb_2.ogg" title="dog pronunciation
                    English" style="cursor: pointer" valign="top">&nbsp;</div><span class="phon">/dɒɡ/</span></div>
"""
HTML_WITHOUT_DIV = """<span class="phon">/dɒɡ/</span>"""
HTML_WITHOUT_SPAN = """
<div class="phons_br" wd="dog" htag="div" geo="br" hclass="phons_br"><div class="sound audio_play_button pron-uk icon-audio" data-src-mp3="https://www.oxfordlearnersdictionaries.com/media/english/uk_pron/d/dog/dog__/dog__gb_2.mp3" data-src-ogg="https://www.oxfordlearnersdictionaries.com/media/english/uk_pron_ogg/d/dog/dog__/dog__gb_2.ogg" title="dog pronunciation
                    English" style="cursor: pointer" valign="top">&nbsp;</div>
"""


@pytest.fixture(scope="package")
def mock_oxford_response_successful_get():
    with patch(
        "httpx.AsyncClient.get",
        return_value=httpx.Response(status_code=200, text=SUCCESS_HTML),
    ) as mock:
        yield mock


@pytest.fixture(scope="package")
def mock_oxford_response(request):
    def _mock_oxford_response(status_code: int, text: str):
        patcher = patch(
            "httpx.AsyncClient.get",
            return_value=httpx.Response(status_code=status_code, text=text),
        )
        mock = patcher.start()
        request.addfinalizer(patcher.stop)
        return mock

    return _mock_oxford_response


@pytest.fixture
def vocabulary_dog():
    return Vocabulary("dog", "/dɔːɡ/", "", "", "", "", "")


@pytest.fixture
def vocabulary_cat():
    return Vocabulary("cat", "/kæt/", "", "", "", "", "")


@pytest.fixture
def mock_gen_oxford_response():
    def _mock():
        response = [
            httpx.Response(
                status_code=200, text='<div class="phons_br" ><span>/dɒɡ/</span></div>'
            ),
            httpx.Response(
                status_code=200, text='<div class="phons_br"><span>/kæt/</span></div>'
            ),
        ]
        patcher = patch("httpx.AsyncClient.get", side_effect=response)
        mock = patcher.start()
        yield mock
        patcher.stop()

    return _mock
