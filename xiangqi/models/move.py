from django.db import models


class Move(models.Model):
    game = models.ForeignKey('game', on_delete=models.CASCADE)
    participant = models.ForeignKey('participant', on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    notation = models.CharField(max_length=32, null=True)
    origin = models.ForeignKey(
        'position', related_name='+', null=True, on_delete=models.PROTECT
    )
    destination = models.ForeignKey(
        'position', related_name='+', on_delete=models.PROTECT
    )
