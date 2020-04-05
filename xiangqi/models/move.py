from django.db import models
from xiangqi.models import Player


class Move(models.Model):
    class Meta:
        ordering = ["pk"]

    game = models.ForeignKey("game", on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    player = models.ForeignKey('auth.user', on_delete=models.CASCADE)
