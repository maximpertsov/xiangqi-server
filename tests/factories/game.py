from factory import DjangoModelFactory, Sequence, SubFactory
from xiangqi.models import Game

from .player import PlayerFactory


class GameFactory(DjangoModelFactory):
    class Meta:
        model = Game
        django_get_or_create = ("slug",)

    slug = Sequence(lambda n: "GAME{}".format(n))
    player1 = SubFactory(PlayerFactory)
    player2 = SubFactory(PlayerFactory)
