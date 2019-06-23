from django.db import models
from django.utils.crypto import get_random_string


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
        kwargs['slug'] = self._generate_slug() if slug is None else slug
        return super().create(**kwargs)


class Game(models.Model):
    objects = GameManager()

    slug = models.CharField(
        max_length=64, unique=True, editable=False, blank=False, null=False
    )
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    player_limit = models.PositiveIntegerField(default=2)
    created_by = models.ForeignKey('player', on_delete=models.CASCADE, related_name='+')
    participants = models.ManyToManyField(through='participant', to='player')
    board_dimensions = models.CharField(max_length=128)
    move_time_limit = models.CharField(max_length=128, null=True)
    game_time_limit = models.CharField(max_length=128, null=True)
    result = models.ForeignKey('result', on_delete=models.CASCADE, null=True)
