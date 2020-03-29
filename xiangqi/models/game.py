from django.db import models
from django.utils.crypto import get_random_string
from django_fsm import FSMField, transition


class GameManager(models.Manager):
    def _generate_slug(self):
        size = 8
        while True:
            slug = get_random_string(size)
            if self.filter(slug=slug).exists():
                size += 1
                continue
            return slug

    def create(self, slug=None, **kwargs):
        kwargs["slug"] = self._generate_slug() if slug is None else slug
        return super().create(**kwargs)

    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class Game(models.Model):
    class State:
        NEW = "new"
        RED_TURN = "red_turn"
        BLACK_TURN = "black_turn"
        ABORTED = "aborted"
        GAME_OVER = "game_over"

    objects = GameManager()

    state = FSMField(default=State.NEW)

    slug = models.CharField(max_length=64, unique=True, editable=False)
    participants = models.ManyToManyField(through="participant", to="player")

    def natural_key(self):
        return self.slug

    def __str__(self):
        return self.slug
