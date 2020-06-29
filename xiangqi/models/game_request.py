from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models

from xiangqi.models import Player


class GameRequest(models.Model):
    # TODO: limit players to 2?
    players = models.ManyToManyField(Player)
    parameters = JSONField()
    closed_at = models.DateTimeField(null=True)
