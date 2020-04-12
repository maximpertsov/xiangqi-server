from factory import DjangoModelFactory, Sequence

from xiangqi.models import Player


class PlayerFactory(DjangoModelFactory):
    class Meta:
        model = Player
        django_get_or_create = ("username",)

    username = Sequence(lambda n: "user{}".format(n))
