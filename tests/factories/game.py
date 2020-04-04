from factory import DjangoModelFactory, Sequence, SubFactory
from xiangqi.models import Game

from .user import UserFactory


class GameFactory(DjangoModelFactory):
    class Meta:
        model = Game
        django_get_or_create = ("slug",)

    slug = Sequence(lambda n: "GAME{}".format(n))
    red_player = SubFactory(UserFactory)
    black_player = SubFactory(UserFactory)
