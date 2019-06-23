from django.db import models
from django.utils.crypto import get_random_string


class GameManager(models.Manager):
    def _generate_xid(self):
        size = 8
        while True:
            xid = get_random_string(size)
            if self.filter(xid=xid).exists():
                size += 1
                continue
            return xid

    def create(self, xid=None, **kwargs):
        kwargs['xid'] = self._generate_xid() if xid is None else xid
        return super().create(**kwargs)


class Game(models.Model):
    objects = GameManager()

    xid = models.CharField(max_length=64, unique=True, editable=False)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    player_limit = models.PositiveIntegerField(default=2)
    created_by = models.ForeignKey('player', on_delete=models.CASCADE, related_name='+')
    participants = models.ManyToManyField(through='participant', to='player')
    board_dimensions = models.CharField(max_length=128)
    move_time_limit = models.CharField(max_length=128, null=True)
    game_time_limit = models.CharField(max_length=128, null=True)
    result = models.ForeignKey('result', on_delete=models.CASCADE, null=True)
