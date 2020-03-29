from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models


class GameEvent(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=128)
    game = models.ForeignKey("game", related_name="event_set", on_delete=models.CASCADE)
    payload = JSONField()
