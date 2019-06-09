from django.contrib.auth import get_user_model
from factory import DjangoModelFactory, Faker, LazyAttribute, SubFactory

from xiangqi import models


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ("username",)

    first_name = Faker('first_name')
    first_name = Faker('last_name')
    email = Faker('email')
    username = LazyAttribute(lambda f: f.email.split('@')[0])


class PlayerFactory(DjangoModelFactory):
    class Meta:
        model = models.Player

    user = SubFactory(UserFactory)
    rating = 1500


class ResultFactory(DjangoModelFactory):
    class Meta:
        model = models.Result

    description = Faker('sentence')


class GameFactory(DjangoModelFactory):
    class Meta:
        model = models.Game

    start_time = None
    end_time = None
    player_limit = 2
    created_by = SubFactory(PlayerFactory)
    board_dimensions = '10,9'
    move_time_limit = None
    game_time_limit = None
    result = None


class ParticipantFactory(DjangoModelFactory):
    class Meta:
        model = models.Participant

    score = 0.0


class PieceFactory(DjangoModelFactory):
    class Meta:
        model = models.Piece


class MoveTypeFactory(DjangoModelFactory):
    class Meta:
        model = models.MoveType


class MoveFactory(DjangoModelFactory):
    class Meta:
        model = models.Move
