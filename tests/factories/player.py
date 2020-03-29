from factory import DjangoModelFactory, SubFactory
from xiangqi.models import Player

from .user import UserFactory


class PlayerFactory(DjangoModelFactory):
    class Meta:
        model = Player
        django_get_or_create = ("user",)

    user = SubFactory(UserFactory)
    rating = 1500
