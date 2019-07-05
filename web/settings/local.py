import itertools

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
CLIENT_DOMAIN = '127.0.0.1'
WHITELIST_DOMAINS = [CLIENT_DOMAIN, 'localhost']
WHITELIST_PORTS = [3000, 5000]
CORS_ORIGIN_WHITELIST = [
    'http://{}:{}'.format(domain, port)
    for domain, port in itertools.product(WHITELIST_DOMAINS, WHITELIST_PORTS)
]

# CSRF
CSRF_TRUSTED_ORIGINS = [CLIENT_DOMAIN]
