from django.db import models
from django.utils.timezone import datetime, timedelta

from xiangqi.lib import jwt

DEFAULT_TOKEN_LIFE = 3600


class TokenManager(models.Manager):
    def create(self, user, **kwargs):
        created_on = datetime.now()
        expires_on = created_on + timedelta(seconds=DEFAULT_TOKEN_LIFE)
        payload = {'sub': user.username, 'exp': expires_on}
        token_string = jwt.encode(payload)
        kwargs.update(string=token_string, created_on=created_on, expires_on=expires_on)
        return super().create(**kwargs)

    def bulk_create(self, *args, **kwargs):
        raise NotImplementedError('Bulk token creation not allowed')

    def save(self, *args, **kwargs):
        raise NotImplementedError('Token editing not allowed')


class Token(models.Model):
    objects = TokenManager()

    string = models.CharField(max_length=255, unique=True)
    created_on = models.DateTimeField()
    expires_on = models.PositiveIntegerField()
