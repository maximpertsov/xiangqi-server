from uuid import uuid4

from django.db import models
from django.utils import timezone

from xiangqi.lib import jwt
from xiangqi.models import Player

ACCESS_TOKEN_LIFE = 60 * 60
REFRESH_TOKEN_LIFE = 60 * 60 * 24 * 60


class BaseToken(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField()
    expires_at = models.DateTimeField()
    token = models.CharField(max_length=255, unique=True)
    player = models.ForeignKey('auth.user', null=True, on_delete=models.SET_NULL)


class AccessTokenManager(models.Manager):
    def create(self, player, **kwargs):
        created_at = timezone.now()
        expires_at = created_at + timezone.timedelta(seconds=ACCESS_TOKEN_LIFE)
        payload = {
            "exp": int(expires_at.timestamp()),
            "iss": int(created_at.timestamp()),
            "sub": player.username,
        }
        token = jwt.encode(payload).decode()
        kwargs.update(
            created_at=created_at, expires_at=expires_at, token=token, player=player
        )
        return super().create(**kwargs)


class AccessToken(BaseToken):
    objects = AccessTokenManager()


class RefreshTokenManager(models.Manager):
    def create(self, player, **kwargs):
        created_at = timezone.now()
        kwargs.update(
            created_at=created_at,
            expires_at=created_at + timezone.timedelta(seconds=REFRESH_TOKEN_LIFE),
            token=uuid4(),
            player=player,
        )
        return super().create(**kwargs)


class RefreshToken(BaseToken):
    objects = RefreshTokenManager()
