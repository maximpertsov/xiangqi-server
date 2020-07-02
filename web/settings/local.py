import dj_database_url

from web.settings.base import *

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {"default": dj_database_url.config(conn_max_age=600)}

# Cache
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}

# CORS configuration
CORS_ORIGIN_WHITELIST = [
    "http://localhost:{}".format(port) for port in [3000, 3002, 5000]
]

# JWT
JWT_AUTH["JWT_SECRET_KEY"] = os.environ["JWT_SECRET"]

# Channels
CHANNEL_LAYERS["default"]["CONFIG"] = {"hosts": [("127.0.0.1", 6379)]}
