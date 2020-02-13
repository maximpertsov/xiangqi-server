from django.db import models


class Move(models.Model):
    game = models.ForeignKey('game', on_delete=models.CASCADE)
    participant = models.ForeignKey('participant', on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    # TODO: this should not be nullable
    name = models.CharField(max_length=10, null=True)
    notation = models.CharField(max_length=32, null=True)
    # TODO: remove field
    origin = models.ForeignKey(
        'position', related_name='+', null=True, on_delete=models.PROTECT
    )
    # TODO: remove field
    destination = models.ForeignKey(
        'position', related_name='+', null=True, on_delete=models.PROTECT
    )
