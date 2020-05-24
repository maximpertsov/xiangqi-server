from factory import DjangoModelFactory, SubFactory

from xiangqi.models import Move

from .game import GameFactory
from .player import PlayerFactory


class MoveFactory(DjangoModelFactory):
    class Meta:
        model = Move

    game = SubFactory(GameFactory)
    uci = "a10a9"
    player = SubFactory(PlayerFactory)
