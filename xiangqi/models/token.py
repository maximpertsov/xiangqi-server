import jwt
from django.conf import settings
from django.db import models

DEFAULT_TOKEN_LIFE = 3600


class TokenManager(models.Manager):
    def create(self, username, **kwargs):
        payload = {'username': username}
        string = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')
        kwargs.update(string=string)
        return super().create(**kwargs)

    def bulk_create(self):
        raise NotImplementedError('Bulk token creation not allowed')


class Token(models.Model):
    string = models.CharField(max_length=255, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    expires_in = models.PositiveIntegerField(
        null=True, default=DEFAULT_TOKEN_LIFE, help_text='In seconds'
    )
