import dj_database_url

from web.settings.base import *

DEBUG = False
ALLOWED_HOSTS = ["api.xchi.online"]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {"default": dj_database_url.config(conn_max_age=None)}

# Cache
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}

# CORS configuration
CLIENT_DOMAIN = os.environ["CLIENT_DOMAIN"]
CORS_ORIGIN_WHITELIST = ["https://{}".format(CLIENT_DOMAIN)]

# CSRF
CSRF_COOKIE_DOMAIN = CLIENT_DOMAIN
CSRF_TRUSTED_ORIGINS = [CLIENT_DOMAIN]

# JWT
JWT_AUTH["JWT_SECRET_KEY"] = os.environ["JWT_SECRET"]
CHANNEL_LAYERS["default"]["CONFIG"] = {"hosts": [os.environ["REDISCLOUD_URL"]]}
