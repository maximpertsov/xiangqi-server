from factory import DjangoModelFactory, SubFactory

from xiangqi.models import GameRequest

from .player import PlayerFactory


class GameRequestFactory(DjangoModelFactory):
    class Meta:
        model = GameRequest

    player = SubFactory(PlayerFactory)
    parameters = {}
