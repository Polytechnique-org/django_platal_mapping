Django-Plat/al connector
========================

Utility to connect to the plat/al database of X.org from a django app.

How to use
----------

Install this app in your virtualenv (using pip).

Alter your `settings.py` as follows:

.. code-block:: python
    import getconf
    CONFIG = getconf.ConfigGetter('###', [os.path.join(BASE_DIR, 'local_settings.ini')])

    INSTALLED_APPS = [
        # other modules
        'platal',
    ]

    # ...

    DATABASES = {
        'default': {
            # ...
        },
        'platal': {
            'ENGINE': 'django.db.backends.' + CONFIG.getstr('plataldb.engine', 'sqlite3'),
            'NAME': CONFIG.getstr('plataldb.name', 'x5dat'),
            'USER': CONFIG.getstr('plataldb.user', 'web'),
            'PASSWORD': CONFIG.getstr('plataldb.password'),
            'HOST': CONFIG.getstr('plataldb.host', '127.0.0.1'),
            'PORT': CONFIG.getstr('plataldb.port', '3306'),
        },
    }

    # Do not manage MySQL databases but manage SQLite ones for tests and local development
    PLATAL_MANAGED = (DATABASES['platal']['ENGINE'] == 'django.db.backends.sqlite3')

    DATABASE_ROUTERS = ['platal.dbrouter.PlatalRouter']

and integrate (and fill) the following content to your `local_settings.ini`::

    [plataldb]
    ; PLATAL_PLATALDB_ENGINE: the engine to use for the database
    engine = mysqldb
    ; PLATAL_PLATALDB_USERNAME: the username to connect to the database
    username = web
    ; PLATAL_PLATALDB_PASSWORD: the password to connect to the database
    password = *********

You can then import `platal.models` and access the Database.
