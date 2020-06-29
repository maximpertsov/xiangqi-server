from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models

from xiangqi.models import Player


class GameRequest(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    parameters = JSONField()
    closed_at = models.DateTimeField(null=True)
