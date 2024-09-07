"""
Quart LibreTranslate
"""
import json

from quart import Quart, current_app
import httpx

class LibreTranslate:

    def __init__(
            self,
            app: Quart | None = None,
            url: str | None = None,
            api_key: str | None = None
    ) -> None:
        if app is not None:
            self.init_app(app, url, api_key)

    def init_app(
            self,
            app: Quart,
            url: str | None = None,
            api_key: str | None = None
    ) -> None:
        """
        Register the extension with the application.
        """
        if url is not None:
            if url[-1] != "/":
                url  += "/"

        app.config.setdefault('LIBRETRANSLATE_URL', url)
        app.config.setdefault('LIBRETRANSLATE_API_KEY', api_key)
        app.extensions['translate'] = self

    @property
    def url(self) -> str:
        """
        The URL to Libre Translate.
        """
        return current_app.config.get('LIBRETRANSLATE_URL')
    
    @property
    def api_key(self) -> str | None:
        """
        The api key for Libre Translate.
        """
        return current_app.config.get("LIBRETRANSLATE_API_KEY")

    async def detect(self):
        pass

    async def languages(self):
        pass

    async def translate(
            self,
            q: str,
            source: str = 'en',
            target: str = 'es',
            format: str = 'text',
            alternates: int = 3,
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
        """
        if not isinstance(q, str):
            raise TypeError('The text to be translated (q) must be a string.')
        
        if not isinstance(source, str):
            raise TypeError('The source must be a string.')
        
        if not isinstance(target, str):
            raise TypeError('The target source must be a string.')
        
        if format != 'text' or format != 'html':
            raise ValueError('Format must be either html or text.')
        
        url = self.url + 'translate'

        data = {
            "q": q,
            "source": source,
            "target": target,
            "format": format,
            "alternates": alternates
        }

        if self.api_key is not None:
            data["api_key"] = self.api_key

        async with httpx.AsyncClient() as client:
            request = await client.request("GET", url, data=data, timeout=timeout)
            response = await request.aread()
            response_str = response.decode()
            await client.aclose()
        
        return json.loads(response_str)["translatedText"]

    async def translate_file(self):
        pass
