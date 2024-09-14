"""
tests.conftest
"""
import pytest

from quart import Quart
from quart_libretranslate import LibreTranslate


@pytest.fixture()
def api_url() -> str:
    """
    Returns the url to connect
    to LibreTranslate.
    """
    return 'http://localhost:5001/'


@pytest.fixture()
def app(api_url: str) -> Quart:
    """
    Creates and returns a `Quart` app
    for testing.
    """
    app = Quart(__name__)
    app.config['TESTING'] = True
    app.config['LIBRETRANSLATE_URL'] = api_url
    return app


@pytest.fixture()
def translate(app: Quart) -> LibreTranslate:
    """
    Creates and returns an instance of
    `quart_libretranslate.LibreTranslate`.
    """
    translate = LibreTranslate(app)
    return translate
