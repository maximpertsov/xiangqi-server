from factory import DjangoModelFactory, SubFactory

from xiangqi.models import Move

from .game import GameFactory
from .participant import ParticipantFactory


class MoveFactory(DjangoModelFactory):
    class Meta:
        model = Move

    game = SubFactory(GameFactory)
    name = "a10a9"
    participant = SubFactory(ParticipantFactory)
