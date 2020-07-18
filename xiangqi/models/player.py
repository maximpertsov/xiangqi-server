from django.contrib.auth.models import User


class Player(User):
    class Meta:
        proxy = True

    def games(self, **filters):
        from xiangqi.models import Game

        return Game.objects.filter(player1=self, **filters).union(
            Game.objects.filter(player2=self, **filters)
        )

    def active_games(self):
        return self.games(finished_at__isnull=True)
