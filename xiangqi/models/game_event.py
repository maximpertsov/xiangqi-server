from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models


class GameEvent(models.Model):
    class Meta:
        indexes = [models.Index(fields=["name", "created_at"])]

    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=128)
    game = models.ForeignKey("game", related_name="event_set", on_delete=models.CASCADE)
    payload = JSONField()
