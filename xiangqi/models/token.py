from uuid import uuid4

from django.db import models
from django.utils import timezone

from xiangqi.lib import jwt
from xiangqi.models import User

DEFAULT_TOKEN_LIFE = 3600

ACCESS_TOKEN_LIFE = 60 * 60
REFRESH_TOKEN_LIFE = 60 * 60 * 24 * 60


class BaseToken(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField()
    expires_at = models.DateTimeField()
    token = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)


class AccessTokenManager(models.Manager):
    def create(self, user, **kwargs):
        created_at = timezone.now()
        expires_at = created_at + timezone.timedelta(seconds=ACCESS_TOKEN_LIFE)
        payload = {
            "exp": int(expires_at.timestamp()),
            "iss": int(created_at.timestamp()),
            "sub": user.username,
        }
        token = jwt.encode(payload).decode()
        kwargs.update(
            created_at=created_at, expires_at=expires_at, token=token, user=user
        )
        return super().create(**kwargs)


class AccessToken(BaseToken):
    objects = AccessTokenManager()


class RefreshTokenManager(models.Manager):
    def create(self, user, **kwargs):
        created_at = timezone.now()
        kwargs.update(
            created_at=created_at,
            expires_at=created_at + timezone.timedelta(seconds=REFRESH_TOKEN_LIFE),
            token=uuid4(),
            user=user,
        )
        return super().create(**kwargs)


class RefreshToken(BaseToken):
    objects = RefreshTokenManager()


class TokenManager(models.Manager):
    def create(self, user, **kwargs):
        created_on = timezone.now()
        expires_on = created_on + timezone.timedelta(seconds=DEFAULT_TOKEN_LIFE)
        payload = {'sub': user.username, 'exp': int(expires_on.timestamp())}
        token_string = jwt.encode(payload).decode()
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
    expires_on = models.DateTimeField()

    # TODO: add to user manager (requires users proxy class)
    def get_user(self):
        user_info = jwt.decode(self.string)
        return User.objects.get(username=user_info['sub'])
