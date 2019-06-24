from django.db import models

from xiangqi.models import Color


class PieceManager(models.Manager):
    def get_by_natural_key(self, name, origin_rank, origin_file):
        return self.get(name=name, origin__rank=origin_rank, origin__file=origin_file)


class Piece(models.Model):
    objects = PieceManager()

    class Meta:
        unique_together = [('name', 'origin')]

    name = models.CharField(max_length=32, db_index=True)
    origin = models.ForeignKey('position', related_name='+', on_delete=models.PROTECT)
    color = models.CharField(max_length=32, choices=Color.choices())

    def natural_key(self):
        return [self.name] + self.origin.natural_key()

    natural_key.dependencies = ['xiangqi.position']

    def __str__(self):
        return self.name
