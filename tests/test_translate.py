"""
tests.test_translate
"""
import pytest

from quart import Quart
from quart_libretranslate import LibreTranslate, ApiError


@pytest.mark.asyncio
async def test_translate_detect(app: Quart) -> None:
    """
    Tests the detect function of LibreTranslate.
    """
    translate: LibreTranslate = app.extensions['translate']

    async with app.app_context():
        detected = await translate.detect('hello')
        assert isinstance(detected, list)
        lang = detected[0]["language"]
        assert lang == 'en'

        detected = await translate.detect('gracias')
        assert isinstance(detected, list)
        lang = detected[0]["language"]
        assert lang == 'es'


@pytest.mark.asyncio
async def test_translate_languages(app: Quart) -> None:
    """
    Tests the languages get function for LibreTranslate.
    """
    translate: LibreTranslate = app.extensions['translate']

    async with app.app_context():
        languages = await translate.languages
        english = languages[0]
        spanish = languages[1]

        assert english['code'] == 'en'
        assert spanish['code'] == 'es'


@pytest.mark.asyncio
async def test_translate_translator(app: Quart) -> None:
    """
    Tests the translate function for
    LibreTranslate.
    """
    translate: LibreTranslate = app.extensions['translate']

    async with app.app_context():
        value = await translate.translate('hello')
        assert value['translatedText'] == 'hola'

        value = await translate.translate('computer')
        assert value['translatedText'] == 'ordenador'
