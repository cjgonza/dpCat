import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'dpcat.db',                      # Or path to database file if using sqlite3.
    }
}

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MEDIA_ROOT = os.path.join(BASE_DIR, 'files')
STATIC_ROOT = os.path.join(MEDIA_ROOT, 'static')

MEDIA_URL = os.path.join(STATIC_ROOT, 'files/')
STATIC_URL = os.path.join(MEDIA_URL, 'static/')