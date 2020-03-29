from factory import DjangoModelFactory, SubFactory

from xiangqi.models import GameEvent

from .game import GameFactory


class GameEventFactory(DjangoModelFactory):
    class Meta:
        model = GameEvent

    game = SubFactory(GameFactory)
    name = "game_created"
    payload = {}
