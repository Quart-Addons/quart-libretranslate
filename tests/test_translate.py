"""
tests.test_translate
"""
import pytest

from quart import Quart
from quart_libretranslate import LibreTranslate


@pytest.mark.asyncio
async def test_translate_detect(
    app: Quart, translate: LibreTranslate
) -> None:
    """
    Tests the detect function of LibreTranslate.
    """
    en_txt = 'hello'
    es_txt = 'halo'

    async with app.app_context():
        detected = await translate.detect(en_txt)
        assert isinstance(detected, list)
        lang = detected[0]["language"]
        assert lang == en_txt
