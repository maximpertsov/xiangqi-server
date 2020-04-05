from factory import DjangoModelFactory, Faker, LazyAttribute
from xiangqi.models import Player


class PlayerFactory(DjangoModelFactory):
    class Meta:
        model = Player
        django_get_or_create = ("username",)

    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email = Faker("email")
    username = LazyAttribute(lambda obj: obj.email.split("@")[0])
