from factory import DjangoModelFactory, SubFactory

from xiangqi.models.game_event import GameEvent

from .game import GameFactory


class GameEventFactory(DjangoModelFactory):
    class Meta:
        model = GameEvent

    game = SubFactory(GameFactory)
    name = "game_created"
    payload = {}
