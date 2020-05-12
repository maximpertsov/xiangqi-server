from django.db import models

from xiangqi.models import Player


class Move(models.Model):
    class Meta:
        ordering = ["pk"]

    fen = models.CharField(max_length=128)
    game = models.ForeignKey("game", on_delete=models.CASCADE)
    gives_check = models.BooleanField()
    name = models.CharField(max_length=10)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    previous_move = models.ForeignKey(
        "move", null=True, on_delete=models.SET_NULL, related_name="next_move_set"
    )
