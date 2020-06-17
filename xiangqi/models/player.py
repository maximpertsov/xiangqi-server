from django.contrib.auth.models import User


class Player(User):
    class Meta:
        proxy = True

    @property
    def games(self):
        from xiangqi.models import Game

        return Game.objects.filter(player1=self).union(
            Game.objects.filter(player2=self)
        )
