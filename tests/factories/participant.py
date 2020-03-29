from factory import DjangoModelFactory, SubFactory
from xiangqi.models import Participant

from .game import GameFactory


class ParticipantFactory(DjangoModelFactory):
    class Meta:
        model = Participant

    game = SubFactory(GameFactory)
    score = 0.0
