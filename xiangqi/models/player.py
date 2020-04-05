from django.contrib.auth.models import User


class Player(User):
    class Meta:
        proxy = True

    @property
    def games(self):
        from xiangqi.models import Game

        return Game.objects.filter(red_player=self).union(
            Game.objects.filter(black_player=self)
        )
