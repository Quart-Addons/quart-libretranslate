"""
Quart LibreTranslate
"""
from typing import Any, Dict, List, Tuple

from quart import Quart, current_app
import httpx


class LibreTranslate:
    """
    LibreTranslate Quart Extension.

    Just a wrapper around the LibreTranslate API.

    Arguments:
        app: The `Quart` application.
        url: The url to Libre Translate. Defaults to ``None``.
        api_key: Libre Translate api key. Default to ``None``.
        timeout: The timeout for the response in seconds. Defaults to ``None``.
    """
    def __init__(
            self,
            app: Quart | None = None,
            url: str | None = None,
            api_key: str | None = None,
            timeout: float | None = None
    ) -> None:
        if app is not None:
            self.init_app(app, url, api_key, timeout)

    def init_app(
            self,
            app: Quart,
            url: str | None = None,
            api_key: str | None = None,
            timeout: float | None = None
    ) -> None:
        """
        Register the extension with the application.

        Arguments:
            app: The `Quart` application.
            url: The url to Libre Translate. Defaults to ``None``.
            api_key: Libre Translate api key. Default to ``None``.
            timeout: The timeout for the response in seconds. Defaults to ``None``.
        """
        if url and not isinstance(url, str):
            raise TypeError("The url must be a string.")

        if api_key and not isinstance(api_key, str):
            raise TypeError("The api key must be a string.")

        if timeout and not isinstance(timeout, float):
            raise TypeError("The timeout must be a float.")

        app.config.setdefault('LIBRETRANSLATE_URL', url)
        app.config.setdefault('LIBRETRANSLATE_API_KEY', api_key)
        app.config.setdefault('LIBRETRANSLATE_TIMEOUT', timeout)

        app.extensions['translate'] = self

    @property
    def _url(self) -> str:
        """
        The URL to Libre Translate.
        """
        url: str = current_app.config.get('LIBRETRANSLATE_URL')

        if url.endswith('/'):
            return url
        else:
            return url + '/'

    @property
    def _api_key(self) -> str | None:
        """
        The api key for Libre Translate.
        """
        return current_app.config.get("LIBRETRANSLATE_API_KEY")

    @property
    def _timeout(self) -> float | None:
        return current_app.config.get('LIBRETRANSLATE_TIMEOUT')

    @property
    def _detect_url(self) -> str:
        return self._url + 'detect'

    @property
    def _languages_url(self) -> str:
        return self._url + 'languages'

    @property
    def _translate_url(self) -> str:
        return self._url + 'translate'

    @property
    def _translate_file_url(self) -> str:
        return self._url + 'translate_file'

    async def detect(self, q: str) -> Tuple[Dict[str, Any], int]:
        """
        Detect the language of single text.

        Arguments:
            q: The text to detect.
            timeout: Request timeout in seconds.
        """
        if not isinstance(q, str):
            raise TypeError("The text to detect (q) must be a string.")

        data = {
            'q': q,
        }

        if self._api_key is not None:
            data['api_key'] = self._api_key

        async with httpx.AsyncClient() as client:
            if self._timeout is not None:
                request = await client.post(self._detect_url, data=data, timeout=self._timeout)
            else:
                request = await client.post(self._detect_url, data=data)

        r_data = request.json()[0]
        return r_data, request.status_code

    async def languages(self) -> List[Dict[str, str]]:
        """
        List of languages available to be used for translating.
        """
        async with httpx.AsyncClient() as client:
            if self._api_key is not None:
                if self._timeout is not None:
                    response = await client.get(
                        self._languages_url, params=self._api_key, timeout=self._timeout
                    )
                else:
                    response = await client.get(self._languages_url, params=self._api_key)
            else:
                if self._timeout is not None:
                    response = await client.get(self._languages_url, timeout=self._timeout)
                else:
                    response = await client.get(self._languages_url)

        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError('Libre Translate did not return any languages and there was an error.')

    async def translate(
            self,
            q: str,
            source: str = 'en',
            target: str = 'es',
            alternates: int = 3,
    ) -> Tuple[Dict[str, str], int]:
        """
        Translate a string.

        Must be called from a route or within app context.

        Arguments:
            q: The text to translate.
            source: The source language code (ISO 639).
            target: The target language code (ISO 639).
            alternates: The number of alternates. Defaults to 3.
            timeout: Request timeout in seconds.
        """
        if not isinstance(q, str):
            raise TypeError('The text to be translated (q) must be a string.')

        if not isinstance(source, str):
            raise TypeError('The source must be a string.')

        if not isinstance(target, str):
            raise TypeError('The target source must be a string.')

        data = {
            "q": q,
            "source": source,
            "target": target,
            "format": 'text',
            "alternates": alternates
        }

        if self._api_key is not None:
            data["api_key"] = self._api_key

        async with httpx.AsyncClient() as client:
            if self._timeout is not None:
                request = await client.post(self._translate_url, data=data, timeout=self._timeout)
            else:
                request = await client.post(self._translate_url, data=data)

        return request.json(), request.status_code

    async def translate_file(self):
        pass
