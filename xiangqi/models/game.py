from django.core.exceptions import ValidationError
from django.db import models
from django.utils.crypto import get_random_string

from xiangqi.models import Player


class GameManager(models.Manager):
    def _generate_slug(self):
        size = 8
        while True:
            slug = get_random_string(size).lower()
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
    objects = GameManager()

    slug = models.CharField(max_length=64, unique=True, editable=False)
    red_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="+")
    black_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="+")

    def natural_key(self):
        return self.slug

    def __str__(self):
        return self.slug

    def clean(self):
        if self.red_player == self.black_player:
            raise ValidationError("Red and black players cannot be the same")
