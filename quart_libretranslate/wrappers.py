"""
quart_libretranslate.wrappers
"""
from typing import Any, Dict, List
from quart import current_app

from .core import LibreTranslate


async def detect(q: str) -> List[Dict[str, Any]]:
    """
    Detects the language of a single string.

    Must be called within app context.

    Argument:
        q: The string to detect the language on.

    Returns:
        The detected languages ex: [{"confidence": 0.6, "language": "en"}]

    Raises:
        `ApiError`
    """
    t: LibreTranslate = current_app.extensions['translate']
    return await t.detect(q)


async def languages() -> List[Dict[str, str]]:
    """
    Retrieve a list of supported languages.

    Must be called within app context.

    Returns:
        A list of available languages ex: [{"code":"en", "name":"English"}]

    Raises:
        `ApiError`
    """
    t: LibreTranslate = current_app.extensions['translate']
    return await t.languages


async def translate(
        q: str, source: str = 'en', target: str = 'es'
) -> Dict[str, Any]:
    """
    Translate a string.

    Must be called within app context.

    Arguments:
        q: The text to translate.
        source: The source language code (ISO 639).
        target: The target language code (ISO 639).

    Returns:
        str: The translated text

    Raises:
        `ApiError`
    """
    t: LibreTranslate = current_app.extensions['translate']
    return await t.translate(q, source, target)
