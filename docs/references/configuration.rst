.. _configuration:

=============
Configuration  
=============

To get started all you need to do is to instantiate a :class:`LibreTranslate`
object after configuring the application::

.. code-block:: python

  from quart import Quart
  from quart_babel import LibreTranslate

  app = Quart(__name__)
  app.config.from_pyfile('mysettings.cfg')
  translator = LibreTranslate(app)

You can also use the factory method of initializing extensions:

.. code-block:: python

  translator.init_app(app)

The LibreTranslate object itself can be used to to change some internal defaults.

.. list-table:: Configuration Variables
    :widths: auto 
    :header-rows: 1

    * - Variable
      - Type
      - Default
      - Description
    * - `LIBRETRANSLATE_URL`
      - ``str``
      - N/A
      - The url to LibreTranslate. This must be provided and if it is not
        the extension will raise a `ValueError`.
    * - `LIBRETRANSLATE_API_KEY`
      - ``str``
      - ``None``
      - The api key for LibreTranslate. This should not be needed
        for local installations.
