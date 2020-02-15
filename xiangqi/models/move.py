from django.db import models


class Move(models.Model):
    game = models.ForeignKey('game', on_delete=models.CASCADE)
    participant = models.ForeignKey('participant', on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    name = models.CharField(max_length=10)
