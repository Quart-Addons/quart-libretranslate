"""
quart_libretranslate.core
"""
import json
from typing import Any, Dict, List, Optional
from quart import Quart, current_app
import httpx

from .error import ApiError

ParamsType = Dict[str, str]


class LibreTranslate:
    """
    This is an extension to use LibreTranslate with Quart.

    It is basically a wrapper around the LibreTranslate API.

    Arguments:
        app: The `Quart` application.
        url: The url to LibreTranslate with the port.
        api_key: The api key for LibreTranslate.
        timeout: The timeout for the response in seconds.
    """
    def __init__(
            self,
            app: Optional[Quart] = None,
            url: Optional[str] = None,
            api_key: Optional[str] = None,
            timeout: Optional[float] = None
    ) -> None:
        self.url = url
        self.api_key = api_key
        self.timeout = timeout

        if app is not None:
            self.init_app(app)

    def init_app(self, app: Quart) -> None:
        """
        Register the extension with the `Quart` application.

        Arguments:
            app: The `Quart` application.
        """
        app.config.setdefault('LIBRETRANSLATE_URL', self.url)
        app.config.setdefault('LIBRETRANSLATE_API_KEY', self.api_key)
        app.config.setdefault('LIBRETRANSLATE_TIMEOUT', self.timeout)

        if app.config.get('LIBRETRANSLATE_URL') is None:
            raise ValueError('The URL to LibreTranslate needs to be provided.')

        if not isinstance(app.config.get('LIBRETRANSLATE_URL'), str):
            raise TypeError('The URL to LibreTranslate needs to be a string.')

        if (app.config.get('LIBRETRANSLATE_API_KEY') and not
                isinstance(app.config.get('LIBRETRANSLATE_API_KEY'), str)):
            raise TypeError('The API Key needs to be a string.')

        if (app.config.get('LIBRETRANSLATE_TIMEOUT') and not
                isinstance(app.config.get('LIBRETRANSLATE_TIMEOUT'), float)):
            raise TypeError('The timeout value needs to be a float.')

        app.extensions['translate'] = self

    @property
    def _url(self) -> str:
        url: str = current_app.config.get('LIBRETRANSLATE_URL')

        if url.endswith('/'):
            return url
        else:
            return url + '/'

    @property
    def _detect_url(self) -> str:
        return self._url + 'detect'

    @property
    def _language_url(self) -> str:
        return self._url + 'language'

    @property
    def _translate_url(self) -> str:
        return self._url + 'translate'

    @property
    def _translate_file_url(self) -> str:
        return self._url + 'translate_file'

    @property
    def _api_key(self) -> Optional[str]:
        return current_app.config.get('LIBRETRANSLATE_API_KEY')

    @property
    def _timeout(self) -> Optional[float]:
        return current_app.config.get('LIBRETRANSLATE_TIMEOUT')

    async def detect(self, q: str) -> List[Dict[str, Any]]:
        """
        Detects the language of a single string.

        Argument:
            q: The string to detect the language on.

        Returns:
            The detected languages ex: [{"confidence": 0.6, "language": "en"}]

        Raises:
            `ApiError`
        """
        params: ParamsType = {'q': q}

        if self._api_key is not None:
            params['api_key'] = self._api_key

        async with httpx.AsyncClient() as client:
            req = await client.post(self._detect_url, data=params, timeout=self._timeout)
            response = req.read().decode()
            r_data = json.loads(response)

        if req.status_code == 200:
            return r_data
        else:
            raise ApiError(r_data['error'], req.status_code)

    async def languages(self) -> List[Dict[str, str]]:
        """
        Retrieve a list of supported languages.

        Returns:
            A list of available languages ex: [{"code":"en", "name":"English"}]

        Raises:
            `ApiError`
        """
        params: ParamsType = dict()

        if self._api_key is not None:
            params['api_key'] = self._api_key

        async with httpx.AsyncClient() as client:
            req = await client.get(self._language_url, params=params, timeout=self._timeout)
            response = req.read().decode()
            r_data = json.loads(response)

        if req.status_code == 200:
            return r_data
        else:
            raise ApiError(r_data["error"], req.status_code)

    async def translate(
            self,
            q: str,
            source: str = 'en',
            target: str = 'es',
    ) -> str:
        """
        Translate a string.

        Arguments:
            q: The text to translate.
            source: The source language code (ISO 639).
            target: The target language code (ISO 639).

        Returns:
            str: The translated text

        Raises:
            `ApiError`
        """
        params: ParamsType = {
            "q": q,
            "source": source,
            "target": target
        }

        if self._api_key is not None:
            params["api_key"] = self._api_key

        async with httpx.AsyncClient() as client:
            req = await client.post(self._translate_url, data=params, timeout=self._timeout)
            response = req.read().decode()
            r_data = json.loads(response)

        if req.status_code == 200:
            return r_data['translatedText']
        else:
            raise ApiError(r_data['error'], req.status_code)
