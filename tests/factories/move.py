from factory import DjangoModelFactory, SubFactory

from xiangqi.models import Move

from .game import GameFactory
from .user import UserFactory


class MoveFactory(DjangoModelFactory):
    class Meta:
        model = Move

    game = SubFactory(GameFactory)
    name = "a10a9"
    player = SubFactory(UserFactory)
