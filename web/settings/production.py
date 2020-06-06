import dj_database_url

from web.settings.base import *

DEBUG = False
ALLOWED_HOSTS = ["api.xchess.xyz"]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {"default": dj_database_url.config(conn_max_age=600)}

# Cache
CACHES = {
    "default": {
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": os.environ["REDISCLOUD_URL"],
    }
}

# CORS configuration
CLIENT_DOMAIN = os.environ["CLIENT_DOMAIN"]
CORS_ORIGIN_WHITELIST = ["https://{}".format(CLIENT_DOMAIN)]

# CSRF
CSRF_COOKIE_DOMAIN = CLIENT_DOMAIN
CSRF_TRUSTED_ORIGINS = [CLIENT_DOMAIN]

# JWT
JWT_AUTH["JWT_SECRET_KEY"] = os.environ["JWT_SECRET"]
