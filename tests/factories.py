import factory as f

from xiangqi import models as m


class UserFactory(f.DjangoModelFactory):
    class Meta:
        model = m.User
        django_get_or_create = ("username",)

    first_name = f.Faker("first_name")
    first_name = f.Faker("last_name")
    email = f.Faker("email")
    username = f.LazyAttribute(lambda obj: obj.email.split("@")[0])


class PlayerFactory(f.DjangoModelFactory):
    class Meta:
        model = m.Player
        django_get_or_create = ("user",)

    user = f.SubFactory(UserFactory)
    rating = 1500


class ResultFactory(f.DjangoModelFactory):
    class Meta:
        model = m.Result

    description = f.Faker("sentence")


class GameFactory(f.DjangoModelFactory):
    class Meta:
        model = m.Game
        django_get_or_create = ("slug",)

    slug = f.Sequence(lambda n: "GAME{}".format(n))


class ParticipantFactory(f.DjangoModelFactory):
    class Meta:
        model = m.Participant

    game = f.SubFactory(GameFactory)
    score = 0.0


class MoveFactory(f.DjangoModelFactory):
    class Meta:
        model = m.Move

    game = f.SubFactory(GameFactory)
    name = "a10a9"
    participant = f.SubFactory(ParticipantFactory)
