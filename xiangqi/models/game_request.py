from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models

from xiangqi.models import Player


class GameRequest(models.Model):
    # TODO: limit players to 2?
    player_set = models.ManyToManyField(Player, related_name='game_request_set')
    parameters = JSONField()
    closed_at = models.DateTimeField(null=True)
