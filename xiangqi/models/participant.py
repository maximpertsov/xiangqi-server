from django.db import models

from xiangqi.models import Color


class ParticipantManager(models.Manager):
    def get_by_natural_key(self, game, color):
        return self.get(game=game, color=color)


class Participant(models.Model):
    objects = ParticipantManager()

    class Meta:
        unique_together = [("game", "color")]

    player = models.ForeignKey('player', on_delete=models.SET_NULL, null=True)
    game = models.ForeignKey('game', on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    color = models.CharField(max_length=32, choices=Color.choices())

    def natural_key(self):
        return (self.game.slug, self.color)

    natural_key.dependencies = ['xiangqi.game']

    def __str__(self):
        player = 'unknown' if self.player is None else self.player
        return '{} ({})'.format(player, self.color)
