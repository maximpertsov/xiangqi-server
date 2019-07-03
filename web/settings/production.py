import dj_database_url

from web.settings.base import *

DEBUG = False
ALLOWED_HOSTS = ['xchess.herokuapp.com']

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

JWT_SECRET = os.environ['JWT_SECRET']

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {'default': dj_database_url.config(conn_max_age=600)}

# Cache
CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}

# CORS configuration
CORS_ORIGIN_WHITELIST = ['https://maximpertsov.github.io']

# JWT configuration
JWT_COOKIE_DOMAIN = 'maximpertsov.github.io'

# CSRF
CSRF_COOKIE_DOMAIN = JWT_COOKIE_DOMAIN
CSRF_TRUSTED_ORIGINS = [CSRF_COOKIE_DOMAIN]
