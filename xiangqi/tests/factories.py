import factory as f
from django.contrib.auth import get_user_model

from xiangqi import models as m


class UserFactory(f.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ("username",)

    first_name = f.Faker('first_name')
    first_name = f.Faker('last_name')
    email = f.Faker('email')
    username = f.LazyAttribute(lambda obj: obj.email.split('@')[0])


class PlayerFactory(f.DjangoModelFactory):
    class Meta:
        model = m.Player
        django_get_or_create = ("user",)

    user = f.SubFactory(UserFactory)
    rating = 1500


class ResultFactory(f.DjangoModelFactory):
    class Meta:
        model = m.Result

    description = f.Faker('sentence')


class GameFactory(f.DjangoModelFactory):
    class Meta:
        model = m.Game
        django_get_or_create = ("slug",)

    slug = f.Sequence(lambda n: 'GAME{}'.format(n))
    start_time = None
    end_time = None
    player_limit = 2
    created_by = f.SubFactory(PlayerFactory)
    board_dimensions = '10,9'
    move_time_limit = None
    game_time_limit = None
    result = None


class ParticipantFactory(f.DjangoModelFactory):
    class Meta:
        model = m.Participant

    score = 0.0


class PieceFactory(f.DjangoModelFactory):
    class Meta:
        model = m.Piece


class MoveTypeFactory(f.DjangoModelFactory):
    class Meta:
        model = m.MoveType


class MoveFactory(f.DjangoModelFactory):
    class Meta:
        model = m.Move
