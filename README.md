# Quart LibreTranslate

![Quart Uploads Logo](logos/logo.png)

This is a basic extension to use [LibreTranslate][] in your Quart app
and is based on [AIOHttp][]. LibreTranslate can be ran on the same server
as your Quart app allowing you not needing a third-party provider. 

# Installation 

Install the extension with the following command:

    $ pip3 install quart-libretranslate

# Usage

To use the extension simply import the class wrapper and pass the Quart app 
object back to here. Do so like this:

    from quart import Quart
    from quart_libretranslate import LibreTranslate

    app = Quart(__name__)
    translate = LibreTranslate(app)


# Documentation

The for Quart-Babel and is available [here][docs].

[LibreTranslate]: https://github.com/LibreTranslate/LibreTranslate
[AIOHttp]: https://docs.aiohttp.org/en/stable/
[docs]: https://quart-libretranslate.readthedocs.io/en/latest/
