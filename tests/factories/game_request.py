from factory import DjangoModelFactory

from xiangqi.models import GameRequest


class GameRequestFactory(DjangoModelFactory):
    class Meta:
        model = GameRequest

    parameters = {}
