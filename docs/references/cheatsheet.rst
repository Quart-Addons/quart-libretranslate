.. _cheatsheet:

==========
Cheatsheet
==========

Basic App
---------

.. code-block:: python

    from quart import Quart, render_template
    from quart_libretranslate import LibreTranslate

    app = Quart(__name__)

    translator = LibreTranslate(app)

    @app.route("/index")
    async def index():
        hello = translator.translate('Hello', source='en', target='es')

        return await render_template('index.html', hello=hello)

Large Applications
------------------

.. code-block:: python
    :caption: yourapplication/routes.py

    from quart import Blueprint 

    bp = Blueprint('main', __name__, url_prefix='/photos')

    @app.route("/index")
    async def index():
        hello = app.extension['translate'].translate(
            'Hello', source='en', target='es'
            )

        return await render_template('index.html', hello=hello)

    # Routes & additional code here. 

.. code-block:: python
    :caption: youapplication/app.py

    from quart import Quart
    from quart_libretranslate import LibreTranslate

    translator = LibreTranslate()

    def create_app() -> Quart:
        app = Quart(__name__)

        translator.init_app(app)

        from .routes import bp as main_bp
        app.register_blueprint(main_bp)

        # Other app registration here. 
        
        return app

Configuration Variables
-----------------------

.. code-block:: python
    :caption: app.py 

    from quart import Quart
    from quart_libretranslate import LibreTranslate

    LIBRETRANSLATE_URL = '192.168.1.90:5000'
    # Use the actual IP & Port for your setup.
    LIBRETRANSLATE_API_KEY = 'jfds944hhg9944'
    # Makes sure you use your actual API key. 
    # Local installs should not need this.

    app = Quart(__name__)
    app.config.from_pyfile(__name__)

    translator = LibreTranslate(app)

    # Setup the rest of the app

Using Translations & Other Language Functions
---------------------------------------------

Please note that these functions need to be
called within app context.

.. code-block:: python

    from quart import quart
    from quart_libretranslate import LibreTranslate, ApiError

    app = Quart(__name__)
    translator = LibreTranslate(app)

    @app.route('/')
    async def index():
        # Detect language of a given word.
        # Returns a list of dictionaries. 
        detected = await translator.detect('hello')

        # Languages available for translating.
        # Returns a list of dictionaries. 
        languages = await translator.languages

        # Translate text - Returns a dictionary.
        t_text = await translator.translate('hello', source="en", target='es')

        # .... Additional route code here, such as return.

Translating & Other Language Functions with Wrappers
----------------------------------------------------
Please note that these functions need to be
called within app context.

Also, we assume that you have the app and extension setup
somewhere else like it has been described above.

.. code-block:: python

    from quart_libretranslate import detect, languages, translate

    app = Quart(__name__)
    translator = LibreTranslate(app)

    @app.route('/')
    async def index():
        # Detect language of a given word.
        # Returns a list of dictionaries. 
        detected = await detect('hello')

        # Languages available for translating.
        # Returns a list of dictionaries. 
        languages = await languages()

        # Translate text - Returns a dictionary.
        t_text = await translate('hello', source="en", target='es')

        # .... Additional route code here, such as return.

