from django.contrib.auth import get_user_model


class User(get_user_model()):
    class Meta:
        proxy = True

    @property
    def games(self):
        from xiangqi.models import Game

        return Game.objects.filter(red_player=self).union(
            Game.objects.filter(black_player=self)
        )
