import dj_database_url

from web.settings.base import *

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

JWT_SECRET = os.environ['JWT_SECRET']

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {'default': dj_database_url.config(conn_max_age=600)}

# Cache
CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}

# CORS configuration
CORS_ORIGIN_WHITELIST = ['http://localhost:3000', 'http://localhost:5000']
