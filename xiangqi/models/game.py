from django.db import models


class Game(models.Model):
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    player_limit = models.PositiveIntegerField(default=2)
    created_by = models.ForeignKey('player', on_delete=models.CASCADE, related_name='+')
    participants = models.ManyToManyField(through='participant', to='player')
    board_dimensions = models.CharField(max_length=128)
    move_time_limit = models.CharField(max_length=128, null=True)
    game_time_limit = models.CharField(max_length=128, null=True)
    result = models.ForeignKey('result', on_delete=models.CASCADE, null=True)
