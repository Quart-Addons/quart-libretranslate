"""
quart_libretranslate.extension
"""
import json
from typing import Dict, List

from quart import Quart, current_app
import httpx

Data = Dict[str, str]


class QuartLibreTranslate:
    """
    LibreTranslate extension for Quart.

    Connect a LibreTranslate API connection.

    Arguments:
        app: The `quart.Quart` app. Defaults to ``None``.
        url: The url to LibreTranslate.
        api_key: LibreTranslate api_key. Defaults to ``None``.
    """
    DEFAULT_URL = "https://translate.argosopentech.com/"

    def __init__(
            self,
            app: Quart | None = None,
            url: str | None = None,
            api_key: str | None = None
    ) -> None:
        self.url = url
        self.api_key = api_key

        if app is not None:
            self.init_app(app)

    def init_app(self, app: Quart) -> None:
        """
        Initialize the extension with the Quart app.

        Arguments:
            app: The ``quart.Quart`` app.
        """
        # Add trailing slash to url if it doesn't have one.
        if self.url is not None:
            if self.url[-1] != "/":
                self.url += "/"

        app.config.setdefault(
            "LIBRETRANSLATE_URL",
            self.DEFAULT_URL if self.url is None else self.url
        )

        app.config.setdefault("LIBRETRANSLATE_API_KEY", self.api_key)

        app.extensions["translate"] = self

    @property
    def libretranslate_url(self) -> str:
        """
        LibreTranslate URL
        """
        return current_app.config.get("LIBRETRANSLATE_URL")

    @property
    def libretranslate_api_key(self) -> str | None:
        """
        LibreTranslate API Key
        """
        return current_app.config.get("LIBRETRANSLATE_API_KEY")

    async def translate(
            self,
            q: str,
            source: str = "en",
            target: str = "es",
            timeout: int | None = None
    ) -> str:
        """
        Translate a string.

        Must be called from a route or within app context.

        Arguments:
            q: The text to translate.
            source: The source language code (ISO 639).
            target: The target language code (ISO 639).
            timeout: Request timeout in seconds.

        Returns:
            The translated text as a string.
        """
        url = self.libretranslate_url + "translate"
        data: Data = {"q": q, "source": source, "target": target}

        if self.libretranslate_api_key is not None:
            data["api_key"] = self.libretranslate_api_key

        async with httpx.AsyncClient() as client:
            request = await client.request("GET", url, data=data, timeout=timeout)
            response = await request.aread()
            response_str = response.decode()
            await client.aclose()

        return json.loads(response_str)["translatedText"]

    async def detect(self, q: str, timeout: int | None = None) -> List[Dict[str, str]]:
        """
        Detect the language of a single text.

        Arguments:
            q: Text to detect.
            timeout: Request timeout in seconds.

        Returns:
            The detected languages ex: [{"confidence": 0.6, "language": "en"}]
        """
        url = self.libretranslate_url + "detect"
        data: Data = {"q": q}

        if self.libretranslate_api_key is not None:
            data["api_key"] = self.libretranslate_api_key

        async with httpx.AsyncClient() as client:
            request = await client.request("GET", url, data=data, timeout=timeout)
            response = await request.aread()
            response_str = response.decode()
            await client.aclose()

        return json.loads(response_str)

    async def languages(self, timeout: int | None = None) -> List[Dict[str, str]]:
        """
        Retrieve a list of supported languages.

        Arguments:
            timeout: Request timeout in seconds.

        Returns:
            A list of available languages ex: [{"code":"en", "name":"English"}]
        """
        url = self.libretranslate_url + "languages"
        data: Data = dict()

        if self.libretranslate_api_key is not None:
            data["api_key"] = self.libretranslate_api_key

        async with httpx.AsyncClient() as client:
            request = await client.request("GET", url, data=data, timeout=timeout)
            response = await request.aread()
            response_str = response.decode()
            await client.aclose()

        return json.loads(response_str)
