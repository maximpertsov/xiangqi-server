from enum import Enum

from django.contrib.auth import get_user_model
from django.db import models


class Color(Enum):
    RED = 'red'
    BLACK = 'black'

    @classmethod
    def choices(cls):
        return [(tag, tag.value) for tag in cls]


class Player(models.Model):
    # TODO set all player attributes to 'anonymous' after a user is deleted
    user = models.OneToOneField(get_user_model(), on_delete=models.SET_NULL, null=True)
    rating = models.PositiveIntegerField()


class Result(models.Model):
    description = models.TextField()


class PositionManager(models.Manager):
    def get_by_natural_key(self, rank, file):
        return self.get(rank=rank, file=file)


# TODO: make this immutable
class Position(models.Model):
    objects = PositionManager()

    class Meta:
        unique_together = [("rank", "file")]

    rank = models.PositiveIntegerField(db_index=True)
    file = models.PositiveIntegerField(db_index=True)

    def natural_key(self):
        return (self.rank, self.file)


class Game(models.Model):
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    player_limit = models.PositiveIntegerField(default=2)
    created_by = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='+')
    participants = models.ManyToManyField(through='Participant', to=Player)
    board_dimensions = models.CharField(max_length=128)
    move_time_limit = models.CharField(max_length=128, null=True)
    game_time_limit = models.CharField(max_length=128, null=True)
    result = models.ForeignKey(Result, on_delete=models.CASCADE, null=True)


class Participant(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    role = models.CharField(max_length=32)
    color = models.CharField(max_length=32, choices=Color.choices())


class Piece(models.Model):
    name = models.CharField(max_length=32)
    origin = models.ForeignKey(Position, related_name='+', on_delete=models.PROTECT)
    color = models.CharField(max_length=32, choices=Color.choices())


class MoveType(models.Model):
    name = models.CharField(max_length=64)


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
