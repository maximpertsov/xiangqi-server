from django.db import models

from xiangqi.models import Game, MoveType, Participant, Piece, Position


class Move(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE)
    type = models.ForeignKey(MoveType, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    notation = models.CharField(max_length=32)
    origin = models.ForeignKey(
        Position, related_name='+', null=True, on_delete=models.PROTECT
    )
    destination = models.ForeignKey(
        Position, related_name='+', on_delete=models.PROTECT
    )
