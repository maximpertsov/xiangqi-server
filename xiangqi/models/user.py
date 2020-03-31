from django.contrib.auth import get_user_model
from django.db import models


class UserManager(models.Manager):
    def get_by_natural_key(self, username):
        return self.get(username=username)


class User(get_user_model()):
    class Meta:
        proxy = True

    objects = UserManager()

    def natural_key(self):
        return self.username

    @property
    def games(self):
        from xiangqi.models import Game

        return Game.objects.filter(red_player=self).union(
            Game.objects.filter(black_player=self)
        )
