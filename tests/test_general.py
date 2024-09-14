"""
tests.test_general
"""
import pytest

from quart import Quart
from quart_libretranslate import LibreTranslate


def test_translate_url(api_url: str, app: Quart) -> None:
    """
    Tests the urls are correct from the
    extension.
    """
    assert app.config['LIBRETRANSLATE_URL'] == api_url


@pytest.mark.asyncio
async def test_translate_urls(
    api_url: str,
    app: Quart,
    translate: LibreTranslate
) -> None:
    """
    Test the different urls to connect to
    LibreTranslate.
    """
    # pylint: disable=W0212
    # pylint: disable=W0104
    detect_url = api_url + 'detect'
    language_url = api_url + 'language'
    translate_url = api_url + 'translate'
    translate_file = api_url + 'translate_file'

    async with app.app_context():
        translate._url == api_url
        translate._detect_url == detect_url
        translate._language_url == language_url
        translate._translate_url == translate_url
        translate._translate_file_url == translate_file
