from django.db import models


class Move(models.Model):
    class Meta:
        ordering = ["pk"]

    game = models.ForeignKey("game", on_delete=models.CASCADE)
    participant = models.ForeignKey("participant", on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
