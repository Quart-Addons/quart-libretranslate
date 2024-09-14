"""
tests.test_wrappers
"""
import pytest
from quart import Quart

from quart_libretranslate import (
    LibreTranslate,
    detect,
    languages,
    translate
)


@pytest.mark.asyncio
async def test_translate_detect_wrap(app: Quart) -> None:
    """
    Tests the detect function of LibreTranslate.
    """
    async with app.app_context():
        detected = await detect('hello')
        assert isinstance(detected, list)
        lang = detected[0]["language"]
        assert lang == 'en'

        detected = await detect('gracias')
        assert isinstance(detected, list)
        lang = detected[0]["language"]
        assert lang == 'es'


@pytest.mark.asyncio
async def test_translate_languages_wrap(app: Quart) -> None:
    """
    Tests the languages get function for LibreTranslate.
    """
    LibreTranslate(app)

    async with app.app_context():
        lang = await languages()
        english = lang[0]
        spanish = lang[1]

        assert english['code'] == 'en'
        assert spanish['code'] == 'es'


@pytest.mark.asyncio
async def test_translate_translator_wrap(app: Quart) -> None:
    """
    Tests the translate function for
    LibreTranslate.
    """
    async with app.app_context():
        value = await translate('hello')
        assert value['translatedText'] == 'hola'

        value = await translate('computer')
        assert value['translatedText'] == 'ordenador'
