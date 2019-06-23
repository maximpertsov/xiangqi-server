from django.db import models

from xiangqi.models import Color


class Piece(models.Model):
    name = models.CharField(max_length=32)
    origin = models.ForeignKey('position', related_name='+', on_delete=models.PROTECT)
    color = models.CharField(max_length=32, choices=Color.choices())
