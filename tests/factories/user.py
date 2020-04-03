from factory import DjangoModelFactory, Faker, LazyAttribute
from xiangqi.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)

    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email = Faker("email")
    username = LazyAttribute(lambda obj: obj.email.split("@")[0])
