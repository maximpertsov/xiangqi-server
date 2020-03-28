from web.settings.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "TEST"

JWT_SECRET = "TEST"

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "circle_test",
        "HOST": "127.0.0.1",
        "PORT": "5432",
        "USERNAME": "circleci",
        "PASSWORD": "",
    }
}

CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}
