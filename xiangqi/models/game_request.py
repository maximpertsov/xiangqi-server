from django.contrib.postgres.fields.jsonb import JSONField
from django.core.exceptions import ValidationError
from django.db import models

from xiangqi.models import Player


class GameRequest(models.Model):
    player1 = models.ForeignKey(
        Player, null=True, on_delete=models.CASCADE, related_name="+"
    )
    player2 = models.ForeignKey(
        Player, on_delete=models.CASCADE, null=True, related_name="+"
    )
    parameters = JSONField()

    def clean(self):
        if self.player1 == self.player2:
            raise ValidationError("Red and black players cannot be the same")
