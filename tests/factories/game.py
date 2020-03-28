from factory import DjangoModelFactory, Sequence
from xiangqi.models import Game


class GameFactory(DjangoModelFactory):
    class Meta:
        model = Game
        django_get_or_create = ("slug",)

    slug = Sequence(lambda n: "GAME{}".format(n))
