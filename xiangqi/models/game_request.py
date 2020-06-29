from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models

from xiangqi.models import Player


class GameRequest(models.Model):
    player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="+")
    player2 = models.ForeignKey(
        Player, on_delete=models.CASCADE, null=True, related_name="+"
    )
    parameters = JSONField()
    closed_at = models.DateTimeField(null=True)
