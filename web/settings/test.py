from web.settings.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'TEST'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'TEST_NAME': ':memory:',
    }
}

CACHES = {'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}
