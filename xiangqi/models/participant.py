from django.db import models

from xiangqi.models import Color


class Participant(models.Model):
    player = models.ForeignKey('player', on_delete=models.CASCADE)
    game = models.ForeignKey('game', on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    role = models.CharField(max_length=32)
    color = models.CharField(max_length=32, choices=Color.choices())
